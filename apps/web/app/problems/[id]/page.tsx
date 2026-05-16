"use client";

import { useEffect, useRef, useState } from "react";
import type * as Monaco from "monaco-editor";
import { useParams, useRouter } from "next/navigation";
import dynamic from "next/dynamic";
import ReactMarkdown from "react-markdown";
import { apiFetch, API_URL } from "@/lib/api";
import { DIFFICULTY_COLOR } from "@/lib/constants";
import { registerSparkSqlCompletions, type SchemaColumn } from "@/lib/sparkSqlCompletions";
import { registerSparkDataframeCompletions } from "@/lib/sparkDataframeCompletions";
import { validateSqlInEditor } from "@/lib/sqlValidator";
import { validatePythonInEditor } from "@/lib/pythonValidator";
import { UserButton, SignInButton, useAuth } from "@clerk/nextjs";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    const codeBlocks = [...text.matchAll(/```(?:\w+)?\n([\s\S]*?)```/g)].map((m) => m[1]).join("\n");
    navigator.clipboard.writeText(codeBlocks || text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };
  return (
    <button
      onClick={handleCopy}
      className="p-1 rounded text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
      title={copied ? "Copied!" : "Copy code"}
    >
      {copied ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="20 6 9 17 4 12" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
        </svg>
      )}
    </button>
  );
}

type Mode = "sql" | "dataframe";
type Preview = Record<string, Record<string, string>[]>;

interface Problem {
  title: string;
  difficulty: string;
  tags: string[];
  description: string;
  schema?: Record<string, SchemaColumn[]>;
  hint_count: number;
  solution_modes: string[];
}

interface Result {
  passed: boolean;
  feedback: string;
  columns?: string[];
  rows?: (string | number | null)[][];
  total_rows?: number;
  truncated?: boolean;
}

const SQL_PLACEHOLDER = "-- Write your Spark SQL query here\nSELECT *\nFROM data\nLIMIT 10";

const DESC_WIDTH_KEY = "spark_practice_desc_width";
const DESC_WIDTH_DEFAULT = 420;
const DESC_WIDTH_MIN = 300;
const DESC_WIDTH_MAX = 900;

const AUTOCOMPLETE_KEY = "spark_practice_autocomplete";
const LIVE_VALIDATION_KEY = "spark_practice_live_validation";

function storageKey(problemId: string, mode: string) {
  return `spark_practice_${problemId}_${mode}`;
}

function loadSavedCode(problemId: string, mode: string): string | null {
  try {
    return localStorage.getItem(storageKey(problemId, mode));
  } catch {
    return null;
  }
}

function saveCode(problemId: string, mode: string, code: string) {
  try {
    localStorage.setItem(storageKey(problemId, mode), code);
  } catch {}
}

function clearSavedCode(problemId: string, mode: string) {
  try {
    localStorage.removeItem(storageKey(problemId, mode));
  } catch {}
}

function dataframePlaceholder(schema: Record<string, SchemaColumn[]>): string {
  const lines: string[] = [];
  const tables = Object.entries(schema);

  for (const [table, cols] of tables) {
    lines.push(`# ${table}: ${cols.map((c) => `${c.column} (${c.type})`).join(", ")}`);
  }
  lines.push("");
  lines.push("# df = first table. F = pyspark.sql.functions. Window = pyspark.sql.window.Window");
  lines.push("# Assign your final DataFrame to 'result'.");
  lines.push("");

  lines.push("result = df \\");
  lines.push("    .select(...) \\");
  lines.push("    .filter(...)")

  return lines.join("\n");
}

const LANGUAGES: Record<Mode, string> = {
  sql: "sql",
  dataframe: "python",
};

export default function ProblemPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { getToken, isSignedIn } = useAuth();
  const [mode, setMode] = useState<Mode>("sql");
  const [code, setCode] = useState(() => {
    if (typeof window === "undefined") return SQL_PLACEHOLDER;
    return loadSavedCode(id, "sql") ?? SQL_PLACEHOLDER;
  });
  const [problem, setProblem] = useState<Problem | null>(null);
  const [preview, setPreview] = useState<Preview | null>(null);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [resultOpen, setResultOpen] = useState(false);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [problemList, setProblemList] = useState<{ id: string }[]>([]);
  const [syntaxError, setSyntaxError] = useState<{ message: string; level: "error" | "warning" } | null>(null);
  const [showSignInBanner, setShowSignInBanner] = useState(false);
  const [hints, setHints] = useState<string[]>([]);
  const [hintIndex, setHintIndex] = useState(-1); // -1 = no hint revealed yet
  const [solution, setSolution] = useState<{ content: string; mode: string } | null>(null);
  const [solutionMode, setSolutionMode] = useState<string>("sql");
  const [holdProgress, setHoldProgress] = useState(0); // 0-100
  const holdTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const sqlCompletionDisposable = useRef<{ dispose: () => void } | null>(null);
  const dfCompletionDisposable = useRef<{ dispose: () => void } | null>(null);
  const monacoRef = useRef<typeof import("monaco-editor") | null>(null);
  const editorRef = useRef<Monaco.editor.IStandaloneCodeEditor | null>(null);
  const sqlValidationTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [descWidth, setDescWidth] = useState<number>(() => {
    if (typeof window === "undefined") return DESC_WIDTH_DEFAULT;
    const saved = Number(localStorage.getItem(DESC_WIDTH_KEY));
    return saved >= DESC_WIDTH_MIN && saved <= DESC_WIDTH_MAX ? saved : DESC_WIDTH_DEFAULT;
  });
  const descWidthRef = useRef(descWidth);
  useEffect(() => { descWidthRef.current = descWidth; }, [descWidth]);
  const [autocompleteOn, setAutocompleteOn] = useState<boolean>(() => {
    if (typeof window === "undefined") return true;
    return localStorage.getItem(AUTOCOMPLETE_KEY) !== "off";
  });
  const [liveValidationOn, setLiveValidationOn] = useState<boolean>(() => {
    if (typeof window === "undefined") return true;
    return localStorage.getItem(LIVE_VALIDATION_KEY) !== "off";
  });
  const liveValidationRef = useRef(liveValidationOn);
  useEffect(() => { liveValidationRef.current = liveValidationOn; }, [liveValidationOn]);

  useEffect(() => {
    Promise.all([
      apiFetch<Problem>(`/problems/${id}`),
      apiFetch<Preview>(`/problems/${id}/preview`),
      apiFetch<{ id: string }[]>("/problems"),
    ])
      .then(([p, pv, list]) => {
        setProblem(p);
        setPreview(pv);
        setProblemList(list);
      })
      .catch(() => setFetchError("Failed to load problem. Is the API running?"));

  }, [id]);

  // Register completions once both editor and schema are available
  useEffect(() => {
    if (!problem?.schema || !monacoRef.current) return;
    sqlCompletionDisposable.current?.dispose();
    dfCompletionDisposable.current?.dispose();
    sqlCompletionDisposable.current = null;
    dfCompletionDisposable.current = null;
    if (!autocompleteOn) return;
    const flatSchema: SchemaColumn[] = Object.entries(problem.schema).flatMap(
      ([table, cols]) => cols.map((c) => ({ ...c, table }))
    );
    sqlCompletionDisposable.current = registerSparkSqlCompletions(monacoRef.current, flatSchema);
    dfCompletionDisposable.current = registerSparkDataframeCompletions(monacoRef.current, flatSchema);
  }, [problem?.schema, monacoRef.current, autocompleteOn]);

  // Reflect autocomplete state in Monaco editor options
  useEffect(() => {
    const editor = editorRef.current;
    if (!editor) return;
    editor.updateOptions({
      quickSuggestions: autocompleteOn,
      suggestOnTriggerCharacters: autocompleteOn,
      wordBasedSuggestions: autocompleteOn ? "currentDocument" : "off",
      parameterHints: { enabled: autocompleteOn },
      inlineSuggest: { enabled: autocompleteOn },
    });
  }, [autocompleteOn]);

  const toggleAutocomplete = () => {
    setAutocompleteOn((prev) => {
      const next = !prev;
      try { localStorage.setItem(AUTOCOMPLETE_KEY, next ? "on" : "off"); } catch {}
      return next;
    });
  };

  // When live validation is turned off, cancel any pending check,
  // clear the banner, and remove existing squiggles.
  useEffect(() => {
    if (liveValidationOn) return;
    if (sqlValidationTimer.current) {
      clearTimeout(sqlValidationTimer.current);
      sqlValidationTimer.current = null;
    }
    setSyntaxError(null);
    const monaco = monacoRef.current;
    const model = editorRef.current?.getModel();
    if (monaco && model) {
      monaco.editor.setModelMarkers(model, "sql-parser", []);
      monaco.editor.setModelMarkers(model, "python-parser", []);
    }
  }, [liveValidationOn]);

  const toggleLiveValidation = () => {
    setLiveValidationOn((prev) => {
      const next = !prev;
      try { localStorage.setItem(LIVE_VALIDATION_KEY, next ? "on" : "off"); } catch {}
      return next;
    });
  };

  const handleModeChange = (m: Mode) => {
    setMode(m);
    const saved = loadSavedCode(id, m);
    setCode(saved ?? (m === "sql" ? SQL_PLACEHOLDER : dataframePlaceholder(problem?.schema ?? {})));
    setResult(null);
    setSyntaxError(null);
  };

  const handleSubmit = async () => {
    setShowSignInBanner(false);
    setLoading(true);
    setResultOpen(true);
    setResult(null);
    const token = await getToken();
    try {
      // SQL mode: validate with Spark analyzer before executing
      if (mode === "sql") {
        const validation = await apiFetch<{ valid: boolean; error: string | null }>(
          `/validate`,
          { method: "POST", body: JSON.stringify({ problem_id: id, code }) },
          token ?? undefined
        );
        if (!validation.valid) {
          setResult({ passed: false, feedback: validation.error ?? "SQL validation failed." });
          setLoading(false);
          return;
        }
      }

      const res = await fetch(`${API_URL}/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { "Authorization": `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ problem_id: id, mode, code }),
      });
      if (!res.ok) throw new Error(`Submit failed: ${res.status}`);
      const data = await res.json();
      setResult(data);

      // Nudge anonymous users to sign in after solving
      if (data.passed && !isSignedIn) {
        setShowSignInBanner(true);
      }
    } catch {
      setResult({ passed: false, feedback: "Failed to reach the server. Try again." });
    } finally {
      setLoading(false);
    }
  };

  const handleNextHint = async () => {
    const nextIndex = hintIndex + 1;
    if (!problem || nextIndex >= problem.hint_count) return;
    if (hints[nextIndex]) {
      setHintIndex(nextIndex);
      return;
    }
    const data = await apiFetch<{ content: string }>(`/problems/${id}/hints/${nextIndex}`);
    setHints((prev) => { const next = [...prev]; next[nextIndex] = data.content; return next; });
    setHintIndex(nextIndex);
  };

  const fetchSolution = async (m: string) => {
    const data = await apiFetch<{ content: string }>(`/problems/${id}/solution/${m}`);
    setSolution({ content: data.content, mode: m });
    setSolutionMode(m);
  };

  const handleHoldStart = () => {
    if (holdTimer.current) return;
    const startTime = Date.now();
    const duration = 3000; // 3 seconds
    holdTimer.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min((elapsed / duration) * 100, 100);
      setHoldProgress(progress);
      if (progress >= 100) {
        clearInterval(holdTimer.current!);
        holdTimer.current = null;
        setHoldProgress(0);
        fetchSolution(solutionMode);
      }
    }, 50);
  };

  const handleHoldEnd = () => {
    if (holdTimer.current) {
      clearInterval(holdTimer.current);
      holdTimer.current = null;
    }
    setHoldProgress(0);
  };

  const currentIndex = problemList.findIndex((p) => p.id === id);
  const prevId = currentIndex > 0 ? problemList[currentIndex - 1].id : null;
  const nextId = currentIndex >= 0 && currentIndex < problemList.length - 1 ? problemList[currentIndex + 1].id : null;

  if (fetchError) {
    return (
      <div className="h-screen flex items-center justify-center bg-[#f7f8fa]">
        <p className="text-sm text-red-400">{fetchError}</p>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-[#f7f8fa] overflow-hidden">
      <header className="h-11 bg-white border-b border-gray-200 flex items-center px-4 shrink-0 gap-4">
        <span className="font-mono text-xs font-bold tracking-widest text-gray-400 uppercase select-none">
          spark.practice
        </span>
        <span className="text-gray-200">|</span>
        <button
          onClick={() => router.push("/problems")}
          className="text-xs text-gray-400 hover:text-gray-700 transition-colors"
        >
          ← Problems
        </button>

        <div className="ml-auto flex items-center gap-4">
          <div className="flex items-center gap-1.5">
          <button
            onClick={() => prevId && router.push(`/problems/${prevId}`)}
            disabled={!prevId}
            className="w-7 h-7 flex items-center justify-center rounded border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm"
          >
            ←
          </button>
          {currentIndex >= 0 && problemList.length > 0 && (
            <span className="text-xs text-gray-400 min-w-9 text-center">
              {currentIndex + 1} / {problemList.length}
            </span>
          )}
          <button
            onClick={() => nextId && router.push(`/problems/${nextId}`)}
            disabled={!nextId}
            className="w-7 h-7 flex items-center justify-center rounded border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm"
          >
            →
          </button>
          </div>
          <span className="text-gray-200">|</span>
          {!isSignedIn ? (
            <SignInButton mode="modal">
              <button className="text-xs text-gray-500 hover:text-gray-800 font-medium transition-colors">Sign in</button>
            </SignInButton>
          ) : (
            <UserButton />
          )}
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden gap-1.5 p-1.5">
        {/* Left — problem panel */}
        <div
          className="shrink-0 bg-white rounded-lg border border-gray-200 flex flex-col overflow-hidden"
          style={{ width: descWidth }}
        >
          <div className="flex border-b border-gray-100 px-4 gap-4">
            <button className="text-xs font-medium text-gray-900 py-3 border-b-2 border-gray-900 -mb-px">
              Description
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-5">
            {problem ? (
              <div className="flex flex-col gap-4">
                <div>
                  <h1 className="text-base font-semibold text-gray-900 mb-2">{problem.title}</h1>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-medium capitalize ${DIFFICULTY_COLOR[problem.difficulty] ?? "text-gray-400"}`}>
                      ● {problem.difficulty}
                    </span>
                    <div className="flex gap-1.5">
                      {problem.tags.map((tag) => (
                        <span key={tag} className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="h-px bg-gray-100" />

                <div className="prose prose-sm prose-gray max-w-none text-gray-700
                  prose-p:leading-relaxed prose-p:my-2
                  prose-strong:text-gray-900 prose-strong:font-semibold
                  prose-code:text-gray-800 prose-code:bg-gray-100 prose-code:px-1 prose-code:rounded prose-code:text-xs
                  prose-code:before:content-none prose-code:after:content-none
                  prose-code:font-normal
                  prose-h2:text-sm prose-h2:font-semibold prose-h2:text-gray-900 prose-h2:mt-4 prose-h2:mb-1">
                  <ReactMarkdown>{problem.description}</ReactMarkdown>
                </div>

                {preview && Object.entries(preview).map(([table, rows]) => {
                  if (!rows.length) return null;
                  const cols = Object.keys(rows[0]);
                  return (
                    <div key={table} className="flex flex-col gap-1.5">
                      <p className="text-xs font-medium text-gray-500">
                        Table: <span className="font-mono text-gray-700">{table}</span>
                      </p>
                      <div className="overflow-x-auto rounded border border-gray-100">
                        <table className="w-full text-xs">
                          <thead className="bg-gray-50 border-b border-gray-100">
                            <tr>
                              {cols.map((col) => (
                                <th key={col} className="px-3 py-1.5 text-left font-medium text-gray-500 font-mono">
                                  {col}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {rows.map((row, i) => (
                              <tr key={i} className="border-t border-gray-50">
                                {cols.map((col) => (
                                  <td key={col} className="px-3 py-1.5 text-gray-600 font-mono">
                                    {row[col]}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })}

                {/* Hints */}
                {problem.hint_count > 0 && (
                  <div className="flex flex-col gap-2">
                    <div className="h-px bg-gray-100" />
                    {hints.slice(0, hintIndex + 1).map((hint, i) => (
                      <div key={i} className="bg-amber-50 border border-amber-100 rounded p-3">
                        <p className="text-xs text-amber-600 font-medium mb-1">Hint {i + 1}</p>
                        <div className="text-xs text-amber-800 prose prose-xs max-w-none
                          prose-code:before:content-none prose-code:after:content-none
                          prose-code:font-normal prose-code:bg-amber-100 prose-code:px-1 prose-code:rounded">
                          <ReactMarkdown>{hint}</ReactMarkdown>
                        </div>
                      </div>
                    ))}
                    {hintIndex < problem.hint_count - 1 && (
                      <button
                        onClick={handleNextHint}
                        className="text-xs font-medium text-left transition-opacity hover:opacity-70"
                        style={{ color: "#3b82f6" }}
                      >
                        {hintIndex === -1 ? "Get a hint →" : `Next hint (${hintIndex + 2}/${problem.hint_count}) →`}
                      </button>
                    )}
                  </div>
                )}

                {/* Solution */}
                {problem.solution_modes.length > 0 && (
                  <div className="flex flex-col gap-2">
                    <div className="h-px bg-gray-100" />
                    {!solution ? (
                      <div className="flex flex-col gap-2">
                        {result?.passed ? (
                          <button
                            onClick={() => fetchSolution(problem.solution_modes[0])}
                            className="text-xs text-emerald-600 hover:text-emerald-700 font-medium text-left"
                          >
                            View solution →
                          </button>
                        ) : (
                          <div className="flex flex-col gap-1.5">
                            <p className="text-xs text-gray-400">Solve the problem to unlock the solution, or hold to reveal.</p>
                            <button
                              onMouseDown={handleHoldStart}
                              onMouseUp={handleHoldEnd}
                              onMouseLeave={handleHoldEnd}
                              className="relative w-full select-none overflow-hidden rounded-lg border border-dashed border-gray-200 px-4 py-3 text-center"
                            >
                              <span className="relative z-10 text-xs font-medium text-gray-400">
                                {holdProgress > 0 ? `Revealing... ${Math.round(holdProgress)}%` : "Hold to reveal solution"}
                              </span>
                              <span
                                className="absolute inset-0 z-0 rounded-lg"
                                style={{
                                  width: `${holdProgress}%`,
                                  background: "linear-gradient(90deg, #eff6ff, #dbeafe)",
                                  transition: holdProgress > 0 ? "width 0.1s linear" : "none",
                                }}
                              />
                            </button>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="flex flex-col gap-2">
                        {problem.solution_modes.length > 1 && (
                          <div className="flex gap-2">
                            {problem.solution_modes.map((m) => (
                              <button
                                key={m}
                                onClick={() => fetchSolution(m)}
                                className={`text-xs px-2 py-1 rounded font-medium ${
                                  solutionMode === m
                                    ? "bg-gray-900 text-white"
                                    : "text-gray-500 hover:text-gray-700"
                                }`}
                              >
                                {m === "sql" ? "SQL" : "DataFrame API"}
                              </button>
                            ))}
                          </div>
                        )}
                        <div className="prose prose-xs prose-gray max-w-none text-xs
                          prose-code:text-gray-800 prose-code:bg-gray-100 prose-code:px-1 prose-code:rounded
                          prose-code:before:content-none prose-code:after:content-none
                          prose-code:font-normal
                          prose-pre:bg-gray-50 prose-pre:border prose-pre:border-gray-100 prose-pre:text-xs">
                          <ReactMarkdown
                            components={{
                              pre({ children }) {
                                const code = ((children as React.ReactElement)?.props as { children?: string })?.children ?? "";
                                return (
                                  <div className="relative">
                                    <div className="absolute -top-6 right-0">
                                      <CopyButton text={code} />
                                    </div>
                                    <pre className="bg-gray-50 border border-gray-100 rounded p-3 text-xs overflow-x-auto">
                                      {children}
                                    </pre>
                                  </div>
                                );
                              },
                            }}
                          >{solution.content}</ReactMarkdown>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full">
                <span className="text-sm text-gray-400">Loading...</span>
              </div>
            )}
          </div>

        </div>

        {/* Vertical resizer between description and editor */}
        <div
          className="w-2 flex items-center justify-center cursor-col-resize group shrink-0"
          onMouseDown={(e) => {
            e.preventDefault();
            const startX = e.clientX;
            const startWidth = descWidth;
            let rafId = 0;
            const onMove = (ev: MouseEvent) => {
              cancelAnimationFrame(rafId);
              rafId = requestAnimationFrame(() => {
                const next = Math.min(
                  Math.max(startWidth + (ev.clientX - startX), DESC_WIDTH_MIN),
                  DESC_WIDTH_MAX,
                );
                setDescWidth(next);
              });
            };
            const onUp = () => {
              cancelAnimationFrame(rafId);
              window.removeEventListener("mousemove", onMove);
              window.removeEventListener("mouseup", onUp);
              try {
                localStorage.setItem(DESC_WIDTH_KEY, String(descWidthRef.current));
              } catch {}
            };
            window.addEventListener("mousemove", onMove);
            window.addEventListener("mouseup", onUp);
          }}
          onDoubleClick={() => {
            setDescWidth(DESC_WIDTH_DEFAULT);
            try { localStorage.setItem(DESC_WIDTH_KEY, String(DESC_WIDTH_DEFAULT)); } catch {}
          }}
          title="Drag to resize · double-click to reset"
        >
          <div className="w-1 h-8 rounded-full bg-gray-200 group-hover:bg-gray-400 transition-colors" />
        </div>

        {/* Right — editor + result panels */}
        <div className="flex-1 flex flex-col overflow-hidden min-w-0">
          <div className={`bg-white rounded-lg border border-gray-200 flex flex-col overflow-hidden ${resultOpen ? "flex-1" : "flex-1"}`}>
            <div className="h-11 border-b border-gray-100 flex items-center justify-between px-4 shrink-0">
              <div className="flex gap-0.5 bg-gray-100 rounded-md p-0.5">
                {(["sql", "dataframe"] as Mode[]).map((m) => (
                  <button
                    key={m}
                    onClick={() => handleModeChange(m)}
                    className={`text-xs px-3 py-1.5 rounded font-medium transition-all ${
                      mode === m
                        ? "bg-white text-gray-900 shadow-sm"
                        : "text-gray-500 hover:text-gray-700"
                    }`}
                  >
                    {m === "sql" ? "SQL" : "DataFrame API"}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={toggleAutocomplete}
                  title={autocompleteOn ? "Autocomplete on — click to turn off" : "Autocomplete off — click to turn on"}
                  className="text-xs px-2 py-1 rounded font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors hidden sm:flex items-center gap-1.5"
                >
                  <span
                    aria-hidden
                    className={`inline-block w-2 h-2 rounded-full ${autocompleteOn ? "bg-emerald-500" : "bg-gray-300"}`}
                  />
                  <span className={autocompleteOn ? "" : "line-through text-gray-400"}>Autocomplete</span>
                </button>
                <button
                  onClick={toggleLiveValidation}
                  title={liveValidationOn ? "Live error check on — click to turn off" : "Live error check off — click to turn on"}
                  className="text-xs px-2 py-1 rounded font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors hidden sm:flex items-center gap-1.5"
                >
                  <span
                    aria-hidden
                    className={`inline-block w-2 h-2 rounded-full ${liveValidationOn ? "bg-emerald-500" : "bg-gray-300"}`}
                  />
                  <span className={liveValidationOn ? "" : "line-through text-gray-400"}>Live errors</span>
                </button>
                <span className="text-xs text-gray-300 hidden sm:block">⌘↵</span>
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className="flex items-center gap-1.5 text-xs font-medium px-4 py-1.5 bg-green-500 hover:bg-green-600 disabled:opacity-60 text-white rounded-md transition-colors"
                >
                  {loading ? (
                    <>
                      <span className="animate-spin inline-block w-3 h-3 border border-white border-t-transparent rounded-full" />
                      Running
                    </>
                  ) : "Run"}
                </button>
              </div>
            </div>

            {/* Sign in banner */}
            {showSignInBanner && (
              <div className="flex items-center justify-between px-4 py-2.5 bg-indigo-50 border-b border-indigo-100 shrink-0">
                <span className="text-xs text-indigo-700 font-medium">{result?.passed ? "🎉 Nice solve! Sign in to save your progress." : "Sign in to submit solutions and track your progress."}</span>
                <div className="flex items-center gap-2">
                  <SignInButton mode="modal">
                    <button className="text-xs font-medium px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded transition-colors">
                      Sign in
                    </button>
                  </SignInButton>
                  <button onClick={() => setShowSignInBanner(false)} className="text-indigo-300 hover:text-indigo-500 text-xs">✕</button>
                </div>
              </div>
            )}

            {/* Syntax error banner */}
            {syntaxError && (
              <div className={`flex items-center gap-2 px-4 py-1.5 border-b text-xs shrink-0 ${
                syntaxError.level === "warning"
                  ? "bg-amber-50 border-amber-100 text-amber-700"
                  : "bg-red-50 border-red-100 text-red-600"
              }`}>
                <span>{syntaxError.level === "warning" ? "⚠" : "✕"}</span>
                <span>{syntaxError.message}</span>
              </div>
            )}

            <div className="flex-1 overflow-hidden">
              <MonacoEditor
                height="100%"
                language={LANGUAGES[mode]}
                value={code}
                onChange={(v) => {
                  const newCode = v ?? "";
                  setCode(newCode);
                  saveCode(id, mode, newCode);
                  if (!liveValidationRef.current) return;
                  if (mode === "sql" && monacoRef.current) {
                    if (sqlValidationTimer.current) clearTimeout(sqlValidationTimer.current);
                    const monaco = monacoRef.current;
                    const editor = editorRef.current;
                    if (!monaco || !editor) return;
                    const model = editor.getModel();
                    if (!model) return;

                    const knownTables = Object.keys(problem?.schema ?? {});

                    // Quick pre-check: if code looks valid, clear error fast (200ms)
                    // Otherwise wait longer before showing error (1000ms)
                    const withoutComments = newCode.replace(/--[^\n]*/g, "").trim();
                    const likelyValid = !!withoutComments && /\bFROM\b/i.test(withoutComments);
                    const delay = likelyValid ? 200 : 1000;

                    sqlValidationTimer.current = setTimeout(() => {
                      const result = validateSqlInEditor(monaco, model, newCode, knownTables);
                      setSyntaxError(result);
                    }, delay);
                  } else if (mode === "dataframe" && monacoRef.current && editorRef.current) {
                    if (sqlValidationTimer.current) clearTimeout(sqlValidationTimer.current);
                    const monaco = monacoRef.current;
                    const model = editorRef.current.getModel();
                    if (!model) return;
                    sqlValidationTimer.current = setTimeout(async () => {
                      const result = await validatePythonInEditor(monaco, model, newCode);
                      setSyntaxError(result);
                    }, 1000);
                  }
                }}
                theme="vs"
                onMount={(editor, monaco) => {
                  monacoRef.current = monaco;
                  editorRef.current = editor;

                  // Cmd+Enter / Ctrl+Enter to run
                  editor.addCommand(
                    monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
                    () => { handleSubmit(); }
                  );

                  if (problem?.schema && autocompleteOn) {
                    const flatSchema: SchemaColumn[] = Object.entries(problem.schema).flatMap(
                      ([table, cols]) => cols.map((c) => ({ ...c, table }))
                    );
                    sqlCompletionDisposable.current?.dispose();
                    dfCompletionDisposable.current?.dispose();
                    sqlCompletionDisposable.current = registerSparkSqlCompletions(monaco, flatSchema);
                    dfCompletionDisposable.current = registerSparkDataframeCompletions(monaco, flatSchema);
                  }

                  // Apply initial autocomplete preference to editor options
                  editor.updateOptions({
                    quickSuggestions: autocompleteOn,
                    suggestOnTriggerCharacters: autocompleteOn,
                    wordBasedSuggestions: autocompleteOn ? "currentDocument" : "off",
                    parameterHints: { enabled: autocompleteOn },
                    inlineSuggest: { enabled: autocompleteOn },
                  });
                }}
                options={{
                  fontSize: 13,
                  fontFamily: "'Geist Mono', 'Fira Code', 'Courier New', monospace",
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  lineNumbers: "on",
                  renderLineHighlight: "line",
                  padding: { top: 16, bottom: 16 },
                  lineNumbersMinChars: 4,
                  lineDecorationsWidth: 16,
                  folding: false,
                  renderWhitespace: "none",
                  scrollbar: { verticalScrollbarSize: 4, horizontalScrollbarSize: 4 },
                  overviewRulerLanes: 0,
                }}
              />
            </div>
          </div>

          {resultOpen && (
            <>
            <div
              className="h-2 flex items-center justify-center cursor-row-resize group shrink-0"
              onMouseDown={(e) => {
                e.preventDefault();
                const container = e.currentTarget.parentElement!;
                const panels = container.children;
                const editorPanel = panels[0] as HTMLElement;
                const resultPanel = panels[2] as HTMLElement;
                const totalHeight = container.clientHeight;
                const initialEditorHeight = editorPanel.offsetHeight;
                const startY = e.clientY;
                let rafId = 0;

                const onMove = (ev: MouseEvent) => {
                  cancelAnimationFrame(rafId);
                  rafId = requestAnimationFrame(() => {
                    const delta = ev.clientY - startY;
                    const newHeight = initialEditorHeight + delta;
                    const min = totalHeight * 0.25;
                    const max = totalHeight * 0.85;
                    const clamped = Math.min(Math.max(newHeight, min), max);
                    editorPanel.style.flex = "none";
                    editorPanel.style.height = `${clamped}px`;
                    resultPanel.style.flex = "1";
                  });
                };
                const onUp = () => {
                  cancelAnimationFrame(rafId);
                  window.removeEventListener("mousemove", onMove);
                  window.removeEventListener("mouseup", onUp);
                };
                window.addEventListener("mousemove", onMove);
                window.addEventListener("mouseup", onUp);
              }}
            >
              <div className="w-8 h-1 rounded-full bg-gray-200 group-hover:bg-gray-400 transition-colors" />
            </div>
            <div className={`bg-white rounded-lg border flex flex-col overflow-hidden flex-1 ${
              result
                ? result.passed ? "border-emerald-200" : "border-red-200"
                : "border-gray-200"
            }`}>
              <div className={`flex items-center justify-between px-4 py-2.5 border-b text-xs font-medium ${
                result
                  ? result.passed
                    ? "border-emerald-100 text-emerald-700 bg-emerald-50"
                    : "border-red-100 text-red-700 bg-red-50"
                  : "border-gray-100 text-gray-500 bg-gray-50"
              }`}>
                <span>{!result ? "Running..." : result.passed ? "✓ Accepted" : "✗ Wrong Answer"}</span>
                <button onClick={() => setResultOpen(false)} className="text-gray-400 hover:text-gray-600">✕</button>
              </div>
              <div className="flex-1 overflow-y-auto">
                {!result ? (
                  <div className="flex items-center gap-2 text-xs text-gray-400 px-4 py-3">
                    <span className="animate-spin inline-block w-3 h-3 border border-gray-300 border-t-gray-600 rounded-full" />
                    Executing on Spark...
                  </div>
                ) : (
                  <div className="flex flex-col">
                    {!result.passed && (
                      <p className="text-xs text-red-500 font-mono whitespace-pre-wrap px-4 py-3 border-b border-gray-50">
                        {result.feedback}
                      </p>
                    )}
                    {result.columns && result.rows && (
                      <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                          <thead className="bg-gray-50 border-b border-gray-100 sticky top-0">
                            <tr>
                              {result.columns.map((col) => (
                                <th key={col} className="px-4 py-2 text-left font-medium text-gray-500 font-mono whitespace-nowrap">
                                  {col}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {result.rows.map((row, i) => (
                              <tr key={i} className="border-t border-gray-50 hover:bg-gray-50">
                                {row.map((cell, j) => (
                                  <td key={j} className="px-4 py-2 text-gray-600 font-mono whitespace-nowrap">
                                    {cell === null ? <span className="text-gray-300 italic">null</span> : String(cell)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                        {result.truncated && (
                          <p className="text-xs text-gray-400 px-4 py-2 border-t border-gray-100">
                            Showing first 100 rows of {result.total_rows} total.
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
