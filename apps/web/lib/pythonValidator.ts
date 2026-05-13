import type * as Monaco from "monaco-editor";
import { API_URL } from "./api";

export interface ValidationResult {
  message: string;
  level: "error" | "warning";
}

export async function validatePythonInEditor(
  monaco: typeof Monaco,
  model: Monaco.editor.ITextModel,
  code: string
): Promise<ValidationResult | null> {
  const withoutComments = code.replace(/#[^\n]*/g, "").trim();
  if (!withoutComments) {
    monaco.editor.setModelMarkers(model, "python-parser", []);
    return null;
  }

  // Import statements are blocked by sandbox — don't flag them here
  if (/^\s*(import |from .+ import)/m.test(code)) {
    monaco.editor.setModelMarkers(model, "python-parser", []);
    return null;
  }

  try {
    const res = await fetch(`${API_URL}/validate/python`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await res.json();

    if (data.valid) {
      monaco.editor.setModelMarkers(model, "python-parser", []);
      return null;
    }

    const line = Math.min(data.line ?? 1, model.getLineCount());
    const message = `Python syntax error: ${data.error}`;
    monaco.editor.setModelMarkers(model, "python-parser", [
      {
        severity: monaco.MarkerSeverity.Error,
        message,
        startLineNumber: line,
        startColumn: 1,
        endLineNumber: line,
        endColumn: model.getLineMaxColumn(line),
      },
    ]);
    return { message, level: "error" };
  } catch {
    return null;
  }
}
