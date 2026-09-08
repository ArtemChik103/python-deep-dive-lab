import React, { useRef, useEffect } from 'react';
import {
  Terminal,
  CheckCircle2,
  XCircle,
  Clock,
  Trash2,
  LineChart,
  Package,
  AlertTriangle,
  Download,
} from 'lucide-react';
import type { EvaluationResponse, ExecutionResult } from '../../types';

interface ConsolePanelProps {
  activeTab: 'output' | 'tests' | 'plots' | 'pip';
  setActiveTab: (tab: 'output' | 'tests' | 'plots' | 'pip') => void;
  execResult: ExecutionResult | null;
  evalResult: EvaluationResponse | null;
  pipLogs: string;
  onClearOutput: () => void;
  isSolutionRevealed?: boolean;
}

export const ConsolePanel: React.FC<ConsolePanelProps> = ({
  activeTab,
  setActiveTab,
  execResult,
  evalResult,
  pipLogs,
  onClearOutput,
  isSolutionRevealed = false,
}) => {
  const plotsCount = execResult?.plots?.length || 0;
  const activeTabRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    activeTabRef.current?.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'nearest',
    });
  }, [activeTab]);

  return (
    <div className="flex flex-col h-full bg-[#141416] border-t border-zinc-800 select-none overflow-hidden">
      {/* Header Tabs */}
      <div className="h-9 bg-zinc-950 border-b border-zinc-800 flex items-center justify-between shrink-0 relative overflow-hidden">
        {/* Scrollable tabs list */}
        <div className="flex-1 flex items-center gap-1 overflow-x-auto no-scrollbar px-2 min-w-0 touch-pan-x h-full">
          <button
            ref={activeTab === 'output' ? activeTabRef : null}
            onClick={() => setActiveTab('output')}
            className={`shrink-0 flex items-center gap-1.5 px-2.5 sm:px-3 py-1 text-xs rounded-md font-medium whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'output'
                ? 'bg-zinc-800 text-zinc-100'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Terminal className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <span className="sm:hidden">Вывод</span>
            <span className="hidden sm:inline">Консоль вывода</span>
            {execResult && (
              <span className="text-[10px] text-zinc-400 font-mono bg-zinc-900 px-1 rounded border border-zinc-700/60">
                {execResult.execution_time_ms}ms
              </span>
            )}
          </button>

          <button
            ref={activeTab === 'tests' ? activeTabRef : null}
            onClick={() => setActiveTab('tests')}
            className={`shrink-0 flex items-center gap-1.5 px-2.5 sm:px-3 py-1 text-xs rounded-md font-medium whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'tests'
                ? 'bg-zinc-800 text-zinc-100'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-sky-400 shrink-0" />
            <span className="sm:hidden">Тесты</span>
            <span className="hidden sm:inline">Результаты тестов</span>
            {evalResult && (
              <span
                className={`text-[10px] font-mono px-1.5 py-0.2 rounded font-semibold ${
                  evalResult.all_passed
                    ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                    : 'bg-rose-950 text-rose-300 border border-rose-800'
                }`}
              >
                {evalResult.passed_tests}/{evalResult.total_tests}
              </span>
            )}
          </button>

          <button
            ref={activeTab === 'plots' ? activeTabRef : null}
            onClick={() => setActiveTab('plots')}
            className={`shrink-0 flex items-center gap-1.5 px-2.5 sm:px-3 py-1 text-xs rounded-md font-medium whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'plots'
                ? 'bg-zinc-800 text-zinc-100'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <LineChart className="w-3.5 h-3.5 text-amber-400 shrink-0" />
            <span className="sm:hidden">Графика</span>
            <span className="hidden sm:inline">Графика (Plots)</span>
            {plotsCount > 0 && (
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 border border-amber-800 font-semibold">
                {plotsCount}
              </span>
            )}
          </button>

          <button
            ref={activeTab === 'pip' ? activeTabRef : null}
            onClick={() => setActiveTab('pip')}
            className={`shrink-0 flex items-center gap-1.5 px-2.5 sm:px-3 py-1 text-xs rounded-md font-medium whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'pip'
                ? 'bg-zinc-800 text-zinc-100'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Package className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
            <span className="sm:hidden">Pip</span>
            <span className="hidden sm:inline">Pip Терминал</span>
          </button>
        </div>

        {/* Pinned Clear output button */}
        <div className="shrink-0 flex items-center px-2 h-full bg-zinc-950 border-l border-zinc-800 z-10 shadow-[-4px_0_6px_-1px_rgba(0,0,0,0.5)]">
          <button
            onClick={onClearOutput}
            className="p-1 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 rounded transition-colors cursor-pointer"
            title="Очистить вывод"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Main Tab Content */}
      <div className="flex-1 overflow-y-auto p-3 font-mono text-xs select-text">
        {/* TAB 1: OUTPUT */}
        {activeTab === 'output' && (
          <div>
            {!execResult ? (
              <div className="text-zinc-500 italic py-2">
                Нажмите «Запустить» (Ctrl+Enter) для выполнения кода...
              </div>
            ) : (
              <div className="space-y-2">
                {/* Meta status bar */}
                <div className="flex items-center gap-3 text-[11px] text-zinc-400 pb-2 border-b border-zinc-800">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3 text-zinc-500" />
                    Время: {execResult.execution_time_ms} ms
                  </span>
                  <span>
                    Код возврата:
                    <span className={`ml-1 font-semibold ${execResult.returncode === 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {execResult.returncode}
                    </span>
                  </span>
                  {execResult.timed_out && (
                    <span className="flex items-center gap-1 text-amber-400 font-bold">
                      <AlertTriangle className="w-3 h-3" />
                      Таймаут выполнения!
                    </span>
                  )}
                </div>

                {/* Stdout */}
                {execResult.stdout && (
                  <pre className="text-zinc-200 whitespace-pre-wrap leading-relaxed">
                    {execResult.stdout}
                  </pre>
                )}

                {/* Stderr */}
                {execResult.stderr && (
                  <pre className="text-rose-400 whitespace-pre-wrap leading-relaxed bg-rose-950/20 p-2.5 rounded-md border border-rose-900/40">
                    {execResult.stderr}
                  </pre>
                )}

                {!execResult.stdout && !execResult.stderr && (
                  <div className="text-zinc-500 italic">Скрипт выполнен без вывода в консоль.</div>
                )}
              </div>
            )}
          </div>
        )}

        {/* TAB 2: TESTS */}
        {activeTab === 'tests' && (
          <div>
            {!evalResult ? (
              <div className="text-zinc-500 italic py-2">
                Нажмите «Проверить тесты» для запуска автогрейдера...
              </div>
            ) : (
              <div className="space-y-3">
                {/* Banner */}
                <div
                  className={`p-3 rounded-lg border flex items-center justify-between ${
                    evalResult.all_passed
                      ? isSolutionRevealed
                        ? 'bg-amber-950/40 border-amber-700/60 text-amber-200'
                        : 'bg-emerald-950/40 border-emerald-700/60 text-emerald-200'
                      : 'bg-rose-950/40 border-rose-700/60 text-rose-200'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {evalResult.all_passed ? (
                      isSolutionRevealed ? (
                        <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
                      ) : (
                        <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                      )
                    ) : (
                      <XCircle className="w-5 h-5 text-rose-400 shrink-0" />
                    )}
                    <div>
                      <div className="font-bold text-sm">
                        {evalResult.all_passed
                          ? isSolutionRevealed
                            ? '📖 Пройдено с эталонным решением (режим ознакомления)'
                            : '🎉 Поздравляем! Все тесты успешно пройдены!'
                          : '⚠️ Решение не прошло проверку'}
                      </div>
                      <div className="text-[11px] opacity-80">
                        Успешно: {evalResult.passed_tests} из {evalResult.total_tests} тестов
                        {isSolutionRevealed && evalResult.all_passed && (
                          <span className="ml-1 text-amber-300 font-medium">
                            • Не идет в зачет честных ачивок
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="text-[11px] font-mono opacity-75">
                    {evalResult.execution_time_ms} ms
                  </div>
                </div>

                {/* Stderr if any */}
                {evalResult.stderr && (
                  <pre className="text-rose-400 whitespace-pre-wrap bg-rose-950/30 p-2.5 rounded border border-rose-900/40">
                    {evalResult.stderr}
                  </pre>
                )}

                {/* Test Cases List */}
                <div className="space-y-1.5">
                  {evalResult.test_cases.map((tc, idx) => (
                    <div
                      key={idx}
                      className={`p-2.5 rounded-md border text-xs space-y-1 ${
                        tc.passed
                          ? 'bg-zinc-950/60 border-zinc-800 text-zinc-300'
                          : 'bg-rose-950/20 border-rose-900/50 text-rose-200'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {tc.passed ? (
                            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                          ) : (
                            <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                          )}
                          <span className="font-semibold text-zinc-200">{tc.name}</span>
                        </div>
                        <span className="text-[10px] text-zinc-500 font-mono">{tc.duration_ms} ms</span>
                      </div>

                      {tc.error && (
                        <div className="mt-1.5 text-rose-300 text-[11px] bg-rose-950/40 p-2 rounded border border-rose-800/40">
                          {tc.error}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 3: PLOTS */}
        {activeTab === 'plots' && (
          <div>
            {plotsCount === 0 ? (
              <div className="text-zinc-500 italic py-2">
                Графики не обнаружены. Попробуйте создать график через <code>matplotlib.pyplot</code> и вызвать <code>plt.show()</code>!
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {execResult?.plots.map((imgSrc, idx) => (
                  <div
                    key={idx}
                    className="p-2 rounded-lg bg-zinc-950 border border-zinc-800 space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs text-zinc-400 px-1">
                      <span>График #{idx + 1}</span>
                      <a
                        href={imgSrc}
                        download={`python_plot_${idx + 1}.png`}
                        className="flex items-center gap-1 text-sky-400 hover:text-sky-300"
                      >
                        <Download className="w-3 h-3" />
                        <span>Скачать</span>
                      </a>
                    </div>
                    <img
                      src={imgSrc}
                      alt={`Captured Plot ${idx + 1}`}
                      className="rounded bg-white max-w-full h-auto mx-auto shadow-sm"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 4: PIP LOGS */}
        {activeTab === 'pip' && (
          <div>
            {!pipLogs ? (
              <div className="text-zinc-500 italic py-2">
                Журнал операций менеджера пакетов Pip пуст.
              </div>
            ) : (
              <pre className="text-zinc-300 whitespace-pre-wrap leading-relaxed">
                {pipLogs}
              </pre>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
