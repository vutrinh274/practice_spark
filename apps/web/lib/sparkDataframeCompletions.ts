import type * as Monaco from "monaco-editor";

const DATAFRAME_METHODS = [
  // Selection & projection
  { label: "select", detail: "Select columns", snippet: "select($1)" },
  { label: "selectExpr", detail: "Select with SQL expressions", snippet: "selectExpr($1)" },
  { label: "drop", detail: "Drop columns", snippet: "drop('$1')" },
  { label: "withColumn", detail: "Add or replace a column", snippet: "withColumn('$1', $2)" },
  { label: "withColumnRenamed", detail: "Rename a column", snippet: "withColumnRenamed('$1', '$2')" },
  // Filtering
  { label: "filter", detail: "Filter rows", snippet: "filter($1)" },
  { label: "where", detail: "Filter rows (alias for filter)", snippet: "where($1)" },
  { label: "distinct", detail: "Return distinct rows", snippet: "distinct()" },
  { label: "dropDuplicates", detail: "Drop duplicate rows", snippet: "dropDuplicates([$1])" },
  { label: "limit", detail: "Limit number of rows", snippet: "limit($1)" },
  // Aggregation
  { label: "groupBy", detail: "Group by columns", snippet: "groupBy($1)" },
  { label: "agg", detail: "Aggregate", snippet: "agg($1)" },
  { label: "count", detail: "Count rows", snippet: "count()" },
  { label: "sum", detail: "Sum a column", snippet: "sum('$1')" },
  { label: "avg", detail: "Average a column", snippet: "avg('$1')" },
  { label: "min", detail: "Min of a column", snippet: "min('$1')" },
  { label: "max", detail: "Max of a column", snippet: "max('$1')" },
  // Sorting
  { label: "orderBy", detail: "Order by columns", snippet: "orderBy($1)" },
  { label: "sort", detail: "Sort by columns", snippet: "sort($1)" },
  // Joins
  { label: "join", detail: "Join with another DataFrame", snippet: "join($1, on='$2', how='inner')" },
  // Set operations
  { label: "union", detail: "Union with another DataFrame", snippet: "union($1)" },
  { label: "unionByName", detail: "Union by column name", snippet: "unionByName($1)" },
  { label: "intersect", detail: "Intersection with another DataFrame", snippet: "intersect($1)" },
  { label: "subtract", detail: "Subtract rows in another DataFrame", snippet: "subtract($1)" },
  // Window
  { label: "withWatermark", detail: "Add watermark for streaming", snippet: "withWatermark('$1', '$2')" },
  // Output / action
  { label: "show", detail: "Print rows to console", snippet: "show($1)" },
  { label: "collect", detail: "Collect rows to driver", snippet: "collect()" },
  { label: "toPandas", detail: "Convert to Pandas DataFrame", snippet: "toPandas()" },
  { label: "printSchema", detail: "Print schema", snippet: "printSchema()" },
  { label: "schema", detail: "Return schema", snippet: "schema" },
  { label: "columns", detail: "Return list of column names", snippet: "columns" },
  { label: "dtypes", detail: "Return list of (name, type) tuples", snippet: "dtypes" },
  { label: "cache", detail: "Cache the DataFrame", snippet: "cache()" },
  { label: "persist", detail: "Persist the DataFrame", snippet: "persist()" },
  { label: "unpersist", detail: "Unpersist the DataFrame", snippet: "unpersist()" },
  { label: "repartition", detail: "Repartition the DataFrame", snippet: "repartition($1)" },
  { label: "coalesce", detail: "Reduce partitions", snippet: "coalesce($1)" },
  { label: "createOrReplaceTempView", detail: "Register as temp SQL view", snippet: "createOrReplaceTempView('$1')" },
  { label: "toDF", detail: "Return new DataFrame with renamed columns", snippet: "toDF($1)" },
  { label: "fillna", detail: "Fill null values", snippet: "fillna($1)" },
  { label: "dropna", detail: "Drop rows with nulls", snippet: "dropna()" },
  { label: "na", detail: "Returns DataFrameNaFunctions", snippet: "na" },
];

const FUNCTIONS_COMPLETIONS = [
  // Aggregate
  "col", "lit", "sum", "count", "avg", "min", "max",
  "collect_list", "collect_set", "approx_count_distinct",
  "countDistinct", "first", "last", "mean",
  // String
  "concat", "concat_ws", "length", "lower", "upper", "trim",
  "ltrim", "rtrim", "substring", "replace", "regexp_replace",
  "split", "explode", "posexplode", "coalesce",
  // Date
  "current_date", "current_timestamp", "date_format",
  "date_add", "date_sub", "datediff", "year", "month",
  "dayofmonth", "hour", "minute", "second", "to_date", "to_timestamp",
  // Math
  "round", "floor", "ceil", "abs", "pow", "sqrt", "log",
  // Window
  "row_number", "rank", "dense_rank", "lag", "lead",
  "first_value", "last_value", "ntile", "percent_rank",
  // Conditional
  "when", "otherwise", "isnull", "isnan",
  // Array
  "array", "array_contains", "size", "sort_array", "array_distinct",
  // Cast
  "cast",
  // Window spec
  "window", "Window",
];

export interface SchemaColumn {
  table: string;
  column: string;
  type: string;
}

export function registerSparkDataframeCompletions(
  monaco: typeof Monaco,
  schema: SchemaColumn[] = []
) {
  const columns = [...new Set(schema.map((c) => c.column))];

  return monaco.languages.registerCompletionItemProvider("python", {
    triggerCharacters: [".", "'", '"'],
    provideCompletionItems(model, position) {
      const lineContent = model.getLineContent(position.lineNumber);
      const textBefore = lineContent.substring(0, position.column - 1);
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn,
      };

      const suggestions: Monaco.languages.CompletionItem[] = [];

      // Trigger DataFrame method completions after a dot
      if (textBefore.endsWith(".") && !textBefore.endsWith("F.")) {
        for (const method of DATAFRAME_METHODS) {
          suggestions.push({
            label: method.label,
            kind: monaco.languages.CompletionItemKind.Method,
            insertText: method.snippet,
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            detail: method.detail,
            range,
          });
        }
        // Also suggest column names as strings after a dot (e.g. df.select('...'))
        for (const col of columns) {
          suggestions.push({
            label: `'${col}'`,
            kind: monaco.languages.CompletionItemKind.Field,
            insertText: `'${col}'`,
            detail: "Column name",
            range,
          });
        }
        return { suggestions };
      }

      // F. completions
      if (textBefore.endsWith("F.")) {
        for (const fn of FUNCTIONS_COMPLETIONS) {
          suggestions.push({
            label: fn,
            kind: monaco.languages.CompletionItemKind.Function,
            insertText: `${fn}($1)`,
            insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
            detail: "pyspark.sql.functions",
            range,
          });
        }
        return { suggestions };
      }

      // Column name string completions inside quotes
      const inSingleQuote = (textBefore.match(/'/g) ?? []).length % 2 === 1;
      const inDoubleQuote = (textBefore.match(/"/g) ?? []).length % 2 === 1;
      if (inSingleQuote || inDoubleQuote) {
        for (const col of columns) {
          suggestions.push({
            label: col,
            kind: monaco.languages.CompletionItemKind.Field,
            insertText: col,
            detail: "Column name",
            range,
          });
        }
        return { suggestions };
      }

      // Top-level: suggest df, F, and common imports
      suggestions.push(
        {
          label: "F",
          kind: monaco.languages.CompletionItemKind.Module,
          insertText: "F",
          detail: "pyspark.sql.functions (imported as F)",
          range,
        },
        {
          label: "df",
          kind: monaco.languages.CompletionItemKind.Variable,
          insertText: "df",
          detail: "Primary DataFrame",
          range,
        }
      );

      return { suggestions };
    },
  });
}
