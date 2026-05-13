import type * as Monaco from "monaco-editor";

const KEYWORDS = [
  "SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "LIMIT",
  "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL OUTER JOIN", "CROSS JOIN",
  "ON", "AS", "DISTINCT", "UNION", "UNION ALL", "INTERSECT", "EXCEPT",
  "CASE", "WHEN", "THEN", "ELSE", "END", "IN", "NOT IN", "IS NULL", "IS NOT NULL",
  "BETWEEN", "LIKE", "AND", "OR", "NOT", "EXISTS", "WITH", "LATERAL VIEW",
  "PARTITION BY", "ROWS BETWEEN", "RANGE BETWEEN", "UNBOUNDED PRECEDING",
  "UNBOUNDED FOLLOWING", "CURRENT ROW", "OVER",
];

const FUNCTIONS = [
  // Aggregate
  "COUNT", "SUM", "AVG", "MIN", "MAX", "COLLECT_LIST", "COLLECT_SET",
  "APPROX_COUNT_DISTINCT", "PERCENTILE_APPROX", "FIRST", "LAST",
  "COUNT_IF", "EVERY", "SOME",
  // Window
  "ROW_NUMBER", "RANK", "DENSE_RANK", "PERCENT_RANK", "CUME_DIST",
  "NTILE", "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE",
  // String
  "CONCAT", "CONCAT_WS", "LENGTH", "LOWER", "UPPER", "TRIM", "LTRIM", "RTRIM",
  "SUBSTRING", "SUBSTR", "REPLACE", "REGEXP_REPLACE", "SPLIT", "EXPLODE",
  "POSEXPLODE", "COALESCE", "NULLIF", "IFNULL", "NVL",
  // Date
  "CURRENT_DATE", "CURRENT_TIMESTAMP", "DATE_FORMAT", "DATE_ADD", "DATE_SUB",
  "DATEDIFF", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND",
  "TO_DATE", "TO_TIMESTAMP", "UNIX_TIMESTAMP", "FROM_UNIXTIME",
  // Math
  "ROUND", "FLOOR", "CEIL", "ABS", "MOD", "POWER", "SQRT", "LOG",
  // Conditional
  "IF", "IFF", "COALESCE", "GREATEST", "LEAST", "NULLIF",
  // Array/Map
  "ARRAY", "MAP", "STRUCT", "SIZE", "ARRAY_CONTAINS", "TRANSFORM",
  "FILTER", "AGGREGATE", "ZIP_WITH", "MAP_KEYS", "MAP_VALUES",
  // Cast
  "CAST", "TRY_CAST",
];

export interface SchemaColumn {
  table: string;
  column: string;
  type: string;
}

export function registerSparkSqlCompletions(
  monaco: typeof Monaco,
  schema: SchemaColumn[] = []
) {
  return monaco.languages.registerCompletionItemProvider("sql", {
    triggerCharacters: [" ", ".", "\n"],
    provideCompletionItems(model, position) {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn,
      };

      const suggestions: Monaco.languages.CompletionItem[] = [];

      // Keywords
      for (const kw of KEYWORDS) {
        suggestions.push({
          label: kw,
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: kw,
          range,
          detail: "Spark SQL keyword",
          sortText: "0" + kw,
        });
      }

      // Functions
      for (const fn of FUNCTIONS) {
        suggestions.push({
          label: fn,
          kind: monaco.languages.CompletionItemKind.Function,
          insertText: `${fn}($1)`,
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          range,
          detail: "Spark SQL function",
          sortText: "1" + fn,
        });
      }

      // Schema columns
      for (const col of schema) {
        suggestions.push({
          label: col.column,
          kind: monaco.languages.CompletionItemKind.Field,
          insertText: col.column,
          range,
          detail: `${col.table}.${col.column} (${col.type})`,
          documentation: `Column from table \`${col.table}\``,
          sortText: "0" + col.column, // surface above functions
        });

        // Also suggest table.column form
        suggestions.push({
          label: `${col.table}.${col.column}`,
          kind: monaco.languages.CompletionItemKind.Field,
          insertText: `${col.table}.${col.column}`,
          range,
          detail: col.type,
          sortText: "0" + col.table + col.column,
        });
      }

      // Table names
      const tables = [...new Set(schema.map((c) => c.table))];
      for (const table of tables) {
        suggestions.push({
          label: table,
          kind: monaco.languages.CompletionItemKind.Module,
          insertText: table,
          range,
          detail: "Table",
          sortText: "0" + table,
        });
      }

      return { suggestions };
    },
  });
}
