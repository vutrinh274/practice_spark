"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { DIFFICULTY_COLOR } from "@/lib/constants";
import { UserButton, SignInButton, useAuth } from "@clerk/nextjs";

interface ProblemSummary {
  id: string;
  title: string;
  difficulty: string;
  tags: string[];
}

export default function ProblemsPage() {
  const router = useRouter();
  const { isSignedIn, isLoaded, getToken } = useAuth();
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSubscriber, setIsSubscriber] = useState<boolean>(false);
  const [accessLoading, setAccessLoading] = useState(true);
  const [solvedSet, setSolvedSet] = useState<Set<string>>(new Set());

  // Fetch problems once on mount
  useEffect(() => {
    apiFetch<ProblemSummary[]>("/problems")
      .then((data) => { setProblems(data); setLoading(false); })
      .catch(() => { setError("Failed to load problems. Is the API running?"); setLoading(false); });
  }, []);

  // Fetch access level when auth state is known
  useEffect(() => {
    if (!isLoaded) return; // Clerk still loading
    if (!isSignedIn) {
      setIsSubscriber(false);
      setSolvedSet(new Set());
      setAccessLoading(false);
      return;
    }
    getToken().then((token) => {
      apiFetch<{ authenticated: boolean; subscriber: boolean }>("/me/access", undefined, token ?? undefined)
        .then((access) => {
          setIsSubscriber(access.subscriber);
          setAccessLoading(false);
          if (access.authenticated) {
            apiFetch<{ problem_id: string; solved: boolean }[]>("/me/progress", undefined, token ?? undefined)
              .then((progress) => {
                setSolvedSet(new Set(progress.filter((p) => p.solved).map((p) => p.problem_id)));
              })
              .catch(() => {});
          }
        })
        .catch(() => { setIsSubscriber(false); setAccessLoading(false); });
    });
  }, [isSignedIn, isLoaded]);

  return (
    <div className="min-h-screen bg-[#f7f8fa]">
      <header className="h-11 bg-white border-b border-gray-200 flex items-center px-6">
        <span className="font-mono text-xs font-bold tracking-widest text-gray-400 uppercase select-none">
          spark.practice
        </span>
        <div className="ml-auto flex items-center gap-3">
          {!isSignedIn ? (
            <SignInButton mode="modal">
              <button className="text-xs text-gray-500 hover:text-gray-800 font-medium transition-colors">Sign in</button>
            </SignInButton>
          ) : (
            <UserButton />
          )}
        </div>
      </header>

      <div className="max-w-3xl mx-auto py-10 px-4">
        <div className="mb-8">
          <h1 className="text-xl font-semibold text-gray-900">Problems</h1>
          <p className="text-sm text-gray-400 mt-1">Practice Spark SQL and DataFrame API</p>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="flex px-5 py-2.5 border-b border-gray-100 text-xs font-medium text-gray-400 uppercase tracking-wide">
            <span className="w-8 shrink-0">#</span>
            <span className="flex-1">Title</span>
            <span className="w-48 shrink-0">Tags</span>
            <span className="w-24 shrink-0">Difficulty</span>
          </div>

          {(loading || accessLoading) && (
            <div className="px-5 py-8 text-sm text-gray-400 text-center">Loading...</div>
          )}

          {error && (
            <div className="px-5 py-8 text-sm text-red-400 text-center">{error}</div>
          )}

          {!loading && !error && !accessLoading && !isSubscriber && (
            <div className="px-5 py-3.5 bg-indigo-50 border-b border-indigo-100 flex items-center justify-between">
              <div className="flex flex-col gap-0.5">
                <span className="text-xs text-indigo-800 font-medium">
                  Unlock {problems.length - 5}{" "}more problems, track your progress &amp; prepare better for Spark interviews.
                </span>
                <span className="text-xs text-indigo-500">
                  ✓{" "}{problems.length}{" "}problems &nbsp;·&nbsp; ✓ Progress tracking &nbsp;·&nbsp; ✓ Submission history
                </span>
              </div>
              <a
                href="https://vutr.substack.com/subscribe?coupon=c08a9839"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs font-medium text-white bg-indigo-600 hover:bg-indigo-700 px-3 py-1.5 rounded transition-colors shrink-0 ml-4"
              >
                Subscribe →
              </a>
            </div>
          )}

          {!loading && !error && !accessLoading && problems.map((problem, index) => {
            const FREE_LIMIT = 5;
            const isLocked = index >= FREE_LIMIT && !isSubscriber;

            if (isLocked) {
              return (
                <div
                  key={problem.id}
                  className="flex px-5 py-3.5 border-b border-gray-50 last:border-0 items-center cursor-default opacity-50"
                >
                  <span className="w-8 shrink-0 text-sm text-gray-300">{index + 1}</span>
                  <span className="flex-1 text-sm font-medium text-gray-400">{problem.title}</span>
                  <div className="w-48 shrink-0" />
                  <div className="w-24 shrink-0">
                    <span className="inline-flex items-center gap-1 text-xs font-medium text-white bg-indigo-500 px-2.5 py-1 rounded-md">
                      <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 1C9.24 1 7 3.24 7 6v1H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2h-2V6c0-2.76-2.24-5-5-5zm0 2c1.66 0 3 1.34 3 3v1H9V6c0-1.66 1.34-3 3-3zm0 10c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2z"/>
                      </svg>
                      Premium
                    </span>
                  </div>
                </div>
              );
            }

            return (
              <div
                key={problem.id}
                onClick={() => router.push(`/problems/${problem.id}`)}
                className="flex px-5 py-3.5 border-b border-gray-50 last:border-0 hover:bg-gray-50 cursor-pointer transition-colors group items-center"
              >
                <span className="w-8 shrink-0 text-sm text-gray-300">{index + 1}</span>
                <span className="flex-1 text-sm font-medium text-gray-800 group-hover:text-gray-900 flex items-center gap-2">
                  {problem.title}
                  {solvedSet.has(problem.id) && (
                    <span className="text-emerald-500 text-xs">✓</span>
                  )}
                </span>
                <div className="w-48 shrink-0 flex gap-1.5 items-center overflow-hidden">
                  <span className="text-xs text-gray-400 bg-gray-100 px-2 py-0.5 rounded truncate max-w-35">
                    {problem.tags[0]}
                  </span>
                  {problem.tags.length > 1 && (
                    <span className="text-xs text-gray-300 shrink-0">+{problem.tags.length - 1}</span>
                  )}
                </div>
                <span className={`w-24 shrink-0 text-xs font-medium capitalize ${DIFFICULTY_COLOR[problem.difficulty] ?? "text-gray-400"}`}>
                  {problem.difficulty}
                </span>
              </div>
            );
          })}

        </div>
      </div>
    </div>
  );
}
