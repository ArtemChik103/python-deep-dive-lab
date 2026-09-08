import React, { useState } from 'react';
import {
  HelpCircle,
  Lightbulb,
  Unlock,
  Eye,
  CheckCircle,
  Clock,
  BookOpen,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  FileCode2,
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import type { HintItem, LessonDetail } from '../../types';

interface TheoryPaneProps {
  lesson: LessonDetail;
  unlockedHints: HintItem[];
  onUnlockNextHint: () => Promise<void>;
  onRevealSolution: () => Promise<void>;
  solution: string | null;
  onApplySolutionToEditor: (solutionCode: string) => void;
  isLoadingHint: boolean;
  isLoadingSolution: boolean;
  onGoToEditor?: () => void;
}

export const TheoryPane: React.FC<TheoryPaneProps> = ({
  lesson,
  unlockedHints,
  onUnlockNextHint,
  onRevealSolution,
  solution,
  onApplySolutionToEditor,
  isLoadingHint,
  isLoadingSolution,
  onGoToEditor,
}) => {
  const [showSolutionConfirm, setShowSolutionConfirm] = useState(false);
  const [copiedSolution, setCopiedSolution] = useState(false);
  const [hintsExpanded, setHintsExpanded] = useState(true);

  const nextHintLevel = unlockedHints.length + 1;
  const hasMoreHints = nextHintLevel <= lesson.total_hints;

  const handleCopySolution = () => {
    if (!solution) return;
    navigator.clipboard.writeText(solution);
    setCopiedSolution(true);
    setTimeout(() => setCopiedSolution(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-zinc-900 overflow-y-auto p-3 sm:p-4 space-y-4 sm:space-y-6 select-text">
      {/* Header Info */}
      <div className="space-y-1.5 border-b border-zinc-800 pb-3">
        <div className="flex items-center gap-2 text-xs text-sky-400 font-medium">
          <BookOpen className="w-3.5 h-3.5" />
          <span className="truncate">{lesson.module_title}</span>
        </div>

        <h1 className="text-base sm:text-lg font-bold text-zinc-100 tracking-tight leading-snug">
          {lesson.title}
        </h1>

        <div className="flex items-center gap-3 text-xs text-zinc-400 pt-1">
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-zinc-500" />
            ~{lesson.estimated_minutes} мин
          </span>
          <span className="capitalize px-2 py-0.5 rounded text-[10px] font-semibold bg-zinc-800 text-zinc-300">
            {lesson.difficulty}
          </span>
        </div>
      </div>

      {/* Task Requirements Box */}
      <div className="rounded-lg bg-sky-950/40 border border-sky-800/60 p-3 sm:p-3.5 space-y-1.5">
        <div className="flex items-center gap-2 text-sky-400 font-semibold text-xs">
          <CheckCircle className="w-4 h-4 shrink-0" />
          <span>Техническое задание:</span>
        </div>
        <p className="text-xs text-sky-100 leading-relaxed">
          {lesson.task_description}
        </p>
      </div>

      {/* Theory Markdown Section */}
      <div className="prose-dark text-xs space-y-3 leading-relaxed">
        <ReactMarkdown
          components={{
            h1: ({ children }) => (
              <h2 className="text-sm sm:text-base font-bold text-white border-b border-zinc-800 pb-1.5 mt-4 mb-2 tracking-tight">
                {children}
              </h2>
            ),
            h2: ({ children }) => (
              <h2 className="text-sm sm:text-base font-bold text-white border-b border-zinc-800 pb-1.5 mt-4 mb-2 tracking-tight">
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3 className="text-xs sm:text-sm font-semibold text-sky-400 mt-3.5 mb-1.5">
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p className="text-xs text-zinc-300 leading-relaxed mb-2.5">
                {children}
              </p>
            ),
            ul: ({ children }) => (
              <ul className="list-disc list-inside space-y-1 text-xs text-zinc-300 pl-1 mb-3">
                {children}
              </ul>
            ),
            ol: ({ children }) => (
              <ol className="list-decimal list-inside space-y-1 text-xs text-zinc-300 pl-1 mb-3">
                {children}
              </ol>
            ),
            li: ({ children }) => (
              <li className="leading-relaxed text-zinc-300">
                {children}
              </li>
            ),
            code: ({ className, children, ...props }) => {
              const isInline = !className && typeof children === 'string' && !children.includes('\n');
              if (isInline) {
                return (
                  <code className="px-1.5 py-0.5 rounded bg-zinc-800 text-sky-300 font-mono text-[11px] border border-zinc-700/60" {...props}>
                    {children}
                  </code>
                );
              }
              return (
                <code className="text-[11px] font-mono text-zinc-200" {...props}>
                  {children}
                </code>
              );
            },
            pre: ({ children }) => (
              <pre className="bg-zinc-950 p-3 rounded-lg border border-zinc-800 overflow-x-auto my-3 text-[11px] font-mono text-zinc-200 shadow-inner">
                {children}
              </pre>
            ),
            strong: ({ children }) => (
              <strong className="font-semibold text-zinc-100">
                {children}
              </strong>
            ),
            hr: () => <hr className="border-zinc-800 my-4" />,
          }}
        >
          {lesson.theory_md}
        </ReactMarkdown>
      </div>

      {/* Progressive Hints Drawer */}
      <div className="rounded-lg bg-zinc-950/70 border border-zinc-800/80 p-3 sm:p-3.5 space-y-2.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-amber-400 shrink-0" />
            <span className="text-xs font-semibold text-zinc-200">
              Подсказки ({unlockedHints.length} / {lesson.total_hints})
            </span>
          </div>

          <button
            onClick={() => setHintsExpanded(!hintsExpanded)}
            className="p-1 text-zinc-400 hover:text-zinc-200 cursor-pointer"
          >
            {hintsExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>

        {hintsExpanded && (
          <div className="space-y-2.5">
            {unlockedHints.map((hint) => (
              <div
                key={hint.level}
                className="rounded-md bg-zinc-900 border border-zinc-800 p-2.5 sm:p-3 text-xs space-y-1 animate-in fade-in duration-200"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-amber-400 flex items-center gap-1.5">
                    <span>Уровень {hint.level}:</span>
                    <span>{hint.title}</span>
                  </span>
                  <span className="text-[10px] text-zinc-500 font-mono">Разблокировано</span>
                </div>
                <div className="text-zinc-300 leading-relaxed mt-1">
                  {hint.content.startsWith('```') ? (
                    <pre className="bg-zinc-950 p-2 rounded text-[11px] font-mono text-sky-300 overflow-x-auto my-1">
                      <code>{hint.content.replace(/```[a-z]*\n?/g, '').trim()}</code>
                    </pre>
                  ) : (
                    hint.content
                  )}
                </div>
              </div>
            ))}

            {hasMoreHints ? (
              <button
                onClick={onUnlockNextHint}
                disabled={isLoadingHint}
                className="w-full flex items-center justify-center gap-2 py-2 px-3 bg-amber-950/50 hover:bg-amber-900/60 border border-amber-800/60 text-amber-300 hover:text-amber-200 rounded-md text-xs font-medium transition-colors cursor-pointer"
              >
                <Unlock className="w-3.5 h-3.5" />
                <span>
                  {isLoadingHint
                    ? 'Загрузка...'
                    : `Открыть подсказку ${nextHintLevel} из ${lesson.total_hints}`}
                </span>
              </button>
            ) : (
              <div className="text-[11px] text-zinc-500 text-center py-1">
                Все доступные подсказки открыты
              </div>
            )}
          </div>
        )}
      </div>

      {/* Solution Section */}
      <div className="rounded-lg bg-zinc-950/70 border border-zinc-800/80 p-3 sm:p-3.5 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Eye className="w-4 h-4 text-indigo-400 shrink-0" />
            <span className="text-xs font-semibold text-zinc-200">
              Эталонное решение
            </span>
          </div>
        </div>

        {solution ? (
          <div className="space-y-3 animate-in fade-in duration-200">
            <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
              <span className="text-emerald-400 font-medium flex items-center gap-1">
                <Check className="w-3.5 h-3.5" />
                Решение открыто
              </span>
              <div className="flex items-center gap-1.5">
                <button
                  onClick={handleCopySolution}
                  className="flex items-center gap-1 px-2 py-1 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 text-[11px] transition-colors cursor-pointer"
                >
                  {copiedSolution ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedSolution ? 'Скопировано' : 'Копировать'}</span>
                </button>
                <button
                  onClick={() => onApplySolutionToEditor(solution)}
                  className="flex items-center gap-1 px-2.5 py-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-medium transition-colors cursor-pointer"
                >
                  Вставить в редактор
                </button>
              </div>
            </div>

            <pre className="bg-zinc-950 p-3 rounded-md border border-zinc-800 overflow-x-auto text-[11px] font-mono text-emerald-300 max-h-60">
              <code>{solution}</code>
            </pre>
          </div>
        ) : showSolutionConfirm ? (
          <div className="p-3 bg-rose-950/40 border border-rose-800/60 rounded-md text-xs space-y-2.5">
            <p className="text-rose-200 font-medium">
              Вы уверены? Попробуйте сначала воспользоваться подсказками или решить задачу самостоятельно.
            </p>
            <div className="flex items-center gap-2">
              <button
                onClick={async () => {
                  await onRevealSolution();
                  setShowSolutionConfirm(false);
                }}
                disabled={isLoadingSolution}
                className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded text-xs font-semibold cursor-pointer"
              >
                {isLoadingSolution ? 'Загрузка...' : 'Да, показать решение'}
              </button>
              <button
                onClick={() => setShowSolutionConfirm(false)}
                className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded text-xs cursor-pointer"
              >
                Попробовать самому
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setShowSolutionConfirm(true)}
            className="w-full flex items-center justify-center gap-2 py-2 px-3 bg-zinc-800/80 hover:bg-zinc-800 text-zinc-300 hover:text-white rounded-md text-xs font-medium transition-colors cursor-pointer"
          >
            <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />
            <span>Не получается решить? Открыть решение</span>
          </button>
        )}
      </div>

      {/* Floating CTA to go straight to Editor on mobile */}
      {onGoToEditor && (
        <div className="pt-2 pb-6">
          <button
            onClick={onGoToEditor}
            className="w-full py-2.5 px-4 bg-sky-600 hover:bg-sky-500 active:bg-sky-700 text-white rounded-lg font-semibold text-xs flex items-center justify-center gap-2 shadow-md transition-colors cursor-pointer"
          >
            <FileCode2 className="w-4 h-4" />
            <span>Перейти к решению в редакторе →</span>
          </button>
        </div>
      )}
    </div>
  );
};
