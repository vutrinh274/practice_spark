import type * as Monaco from "monaco-editor";
import { SparkSQL } from "dt-sql-parser";

const sparkParser = new SparkSQL();

// Conservative semantic rules — only flag things unambiguously wrong in Spark SQL
function checkSemantics(sql: string): string | null {
  const upper = sql.toUpperCase().trim();
  const hasCTE = /^\s*WITH\b/.test(upper);
  const hasSubquery = /\(\s*SELECT\b/.test(upper);

  // Missing FROM — only when non-literal columns referenced, no CTE/subquery
  if (!hasCTE && !hasSubquery && /^SELECT\b/.test(upper) && !/\bFROM\b/.test(upper)) {
    const hasOnlyLiterals = /^SELECT\s+[\d\s,'"*]+$/.test(upper);
    if (!hasOnlyLiterals) {
      return "Missing FROM clause — specify which table to query.";
    }
  }

  // Aggregate + non-aggregate without GROUP BY or window OVER
  const hasGroupBy = /\bGROUP\s+BY\b/.test(upper);
  const hasWindowOver = /\bOVER\s*\(/.test(upper);
  if (!hasGroupBy && !hasWindowOver && !hasCTE && !hasSubquery) {
    const selectClause = upper.match(/SELECT\s+(.*?)\s+FROM\b/s)?.[1] ?? "";
    if (selectClause) {
      const aggregateFns = /\b(SUM|COUNT|AVG|MIN|MAX|COLLECT_LIST|COLLECT_SET|APPROX_COUNT_DISTINCT)\s*\(/;
      const cols = selectClause.split(",").map((c) => c.trim());
      const hasAggregate = cols.some((c) => aggregateFns.test(c));
      const hasNonAggregate = cols.some((c) => !aggregateFns.test(c) && c !== "*");
      if (hasAggregate && hasNonAggregate) {
        return "Missing GROUP BY — mixing aggregate functions with non-aggregated columns.";
      }
    }
  }

  // UNION column count mismatch
  const unionParts = upper.split(/\bUNION\s+(?:ALL\s+|DISTINCT\s+)?/);
  if (unionParts.length > 1) {
    const counts = unionParts.map((part) => {
      const select = part.match(/SELECT\s+(.*?)\s+FROM\b/s)?.[1] ?? "";
      return select ? select.split(",").length : null;
    }).filter(Boolean);
    const allSame = counts.every((c) => c === counts[0]);
    if (!allSame) {
      return "UNION queries must have the same number of columns in each SELECT.";
    }
  }

  // LIMIT with non-numeric value
  const limitMatch = upper.match(/\bLIMIT\s+(\S+)/);
  if (limitMatch && !/^\d+$/.test(limitMatch[1])) {
    return `LIMIT requires a numeric value, got '${limitMatch[1].toLowerCase()}'.`;
  }

  // ORDER BY 0 — always wrong in Spark (1-based)
  if (/\bORDER\s+BY\s+0\b/.test(upper)) {
    return "ORDER BY column index must start at 1, not 0.";
  }

  return null;
}

function setMarker(
  monaco: typeof Monaco,
  model: Monaco.editor.ITextModel,
  line: number,
  message: string
): void {
  const clampedLine = Math.min(Math.max(line, 1), model.getLineCount());
  monaco.editor.setModelMarkers(model, "sql-parser", [
    {
      severity: monaco.MarkerSeverity.Error,
      message,
      startLineNumber: clampedLine,
      startColumn: 1,
      endLineNumber: clampedLine,
      endColumn: model.getLineMaxColumn(clampedLine),
    },
  ]);
}

export interface ValidationResult {
  message: string;
  level: "error" | "warning";
}

export function validateSqlInEditor(
  monaco: typeof Monaco,
  model: Monaco.editor.ITextModel,
  code: string,
  knownTables: string[] = []
): ValidationResult | null {
  const withoutComments = code.replace(/--[^\n]*/g, "").trim();
  if (!withoutComments) {
    monaco.editor.setModelMarkers(model, "sql-parser", []);
    return null;
  }

  // Layer A: Spark SQL parser (dt-sql-parser with SparkSQL dialect)
  const errors = sparkParser.validate(code);
  if (errors.length > 0) {
    const first = errors[0];
    const line = first.startLine ?? 1;
    const message = "SQL syntax error — check for missing keywords, unclosed parentheses, or invalid tokens.";
    setMarker(monaco, model, line, message);
    return { message, level: "error" };
  }

  // Layer B: Conservative semantic checks
  const semanticError = checkSemantics(withoutComments);
  if (semanticError) {
    setMarker(monaco, model, 1, semanticError);
    return { message: semanticError, level: "error" };
  }

  // Layer C: Known table check (warning — yellow, not blocking)
  if (knownTables.length > 0) {
    const upper = withoutComments.toUpperCase();
    const hasCTE = /^\s*WITH\b/.test(upper);
    const hasSubquery = /\(\s*SELECT\b/.test(upper);
    if (!hasCTE && !hasSubquery) {
      const fromMatches = [...withoutComments.matchAll(/\bFROM\s+(\w+)|\bJOIN\s+(\w+)/gi)];
      for (const match of fromMatches) {
        const tableName = (match[1] ?? match[2]).toLowerCase();
        if (!knownTables.map((t) => t.toLowerCase()).includes(tableName)) {
          const warning = `Table \`${tableName}\` not found. Available: ${knownTables.map((t) => `\`${t}\``).join(", ")}.`;
          monaco.editor.setModelMarkers(model, "sql-parser", [
            {
              severity: monaco.MarkerSeverity.Warning,
              message: warning,
              startLineNumber: 1,
              startColumn: 1,
              endLineNumber: model.getLineCount(),
              endColumn: model.getLineMaxColumn(model.getLineCount()),
            },
          ]);
          return { message: warning, level: "warning" };
        }
      }
    }
  }

  monaco.editor.setModelMarkers(model, "sql-parser", []);
  return null;
}
