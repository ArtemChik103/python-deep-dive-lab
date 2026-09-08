import React from 'react';
import {
  Play,
  CheckCircle2,
  Package,
  FolderTree,
  BookOpen,
  FlaskConical,
  RotateCcw,
  Sparkles,
} from 'lucide-react';

interface TopNavbarProps {
  mode: 'curriculum' | 'sandbox';
  setMode: (mode: 'curriculum' | 'sandbox') => void;
  activeSidebarTab: 'curriculum' | 'files' | 'packages';
  setActiveSidebarTab: (tab: 'curriculum' | 'files' | 'packages') => void;
  onRunCode: () => void;
  onRunTests: () => void;
  onResetCode: () => void;
  isRunning: boolean;
  isTesting: boolean;
  completedCount: number;
  totalLessons: number;
  installedPackagesCount: number;
}

export const TopNavbar: React.FC<TopNavbarProps> = ({
  mode,
  setMode,
  activeSidebarTab,
  setActiveSidebarTab,
  onRunCode,
  onRunTests,
  onResetCode,
  isRunning,
  isTesting,
  completedCount,
  totalLessons,
  installedPackagesCount,
}) => {
  const progressPercent = totalLessons > 0 ? Math.round((completedCount / totalLessons) * 100) : 0;

  return (
    <header className="h-14 bg-zinc-900 border-b border-zinc-800 flex items-center justify-between px-4 select-none shrink-0 z-20">
      {/* Brand & Mode Switcher */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center shadow-sm">
            <span className="text-white font-black text-sm tracking-tighter">Py</span>
          </div>
          <div>
            <span className="font-bold text-sm text-zinc-100 tracking-tight">Python Deep Dive</span>
            <span className="ml-1.5 text-xs px-1.5 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800 font-mono font-medium">
              v1.0
            </span>
          </div>
        </div>

        {/* Mode Toggle */}
        <div className="flex items-center bg-zinc-950 p-1 rounded-lg border border-zinc-800">
          <button
            onClick={() => {
              setMode('curriculum');
              setActiveSidebarTab('curriculum');
            }}
            className={`flex items-center gap-1.5 px-3 py-1 text-xs font-medium rounded-md transition-colors ${
              mode === 'curriculum'
                ? 'bg-zinc-800 text-zinc-100 shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-sky-400" />
            Обучение
          </button>
          <button
            onClick={() => {
              setMode('sandbox');
              setActiveSidebarTab('files');
            }}
            className={`flex items-center gap-1.5 px-3 py-1 text-xs font-medium rounded-md transition-colors ${
              mode === 'sandbox'
                ? 'bg-zinc-800 text-zinc-100 shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <FlaskConical className="w-3.5 h-3.5 text-emerald-400" />
            Песочница
          </button>
        </div>
      </div>

      {/* Execution Controls */}
      <div className="flex items-center gap-2">
        <button
          onClick={onRunCode}
          disabled={isRunning || isTesting}
          className="flex items-center gap-2 px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 disabled:opacity-50 text-white text-xs font-semibold rounded-md shadow-xs transition-colors cursor-pointer"
          title="Запустить код (Ctrl + Enter)"
        >
          <Play className={`w-3.5 h-3.5 fill-current ${isRunning ? 'animate-spin' : ''}`} />
          <span>{isRunning ? 'Выполнение...' : 'Запустить'}</span>
          <span className="text-[10px] text-emerald-200 opacity-75 font-mono hidden sm:inline">Ctrl+↵</span>
        </button>

        {mode === 'curriculum' && (
          <button
            onClick={onRunTests}
            disabled={isRunning || isTesting}
            className="flex items-center gap-2 px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 active:bg-sky-700 disabled:opacity-50 text-white text-xs font-semibold rounded-md shadow-xs transition-colors cursor-pointer"
            title="Проверить решение на автоматических тестах"
          >
            <CheckCircle2 className={`w-3.5 h-3.5 ${isTesting ? 'animate-spin' : ''}`} />
            <span>{isTesting ? 'Тестирование...' : 'Проверить тесты'}</span>
          </button>
        )}

        <button
          onClick={onResetCode}
          className="p-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded-md transition-colors"
          title="Сбросить код к исходному"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Right Stats & Drawer Toggles */}
      <div className="flex items-center gap-3">
        {mode === 'curriculum' && (
          <div className="hidden md:flex items-center gap-2 px-2.5 py-1 rounded-md bg-zinc-950 border border-zinc-800">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <div className="flex flex-col text-[11px]">
              <div className="flex items-center gap-1.5">
                <span className="text-zinc-400">Прогресс:</span>
                <span className="font-semibold text-zinc-200">{completedCount} / {totalLessons}</span>
                <span className="text-zinc-500 text-[10px]">({progressPercent}%)</span>
              </div>
              <div className="w-24 h-1.5 bg-zinc-800 rounded-full mt-1 overflow-hidden">
                <div
                  className="h-full bg-emerald-500 transition-all duration-300 rounded-full"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Sidebar Tabs Switchers */}
        <div className="flex items-center bg-zinc-950 p-0.5 rounded-lg border border-zinc-800">
          <button
            onClick={() => setActiveSidebarTab('curriculum')}
            className={`p-1.5 rounded-md transition-colors ${
              activeSidebarTab === 'curriculum'
                ? 'bg-zinc-800 text-sky-400'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
            title="Программа курса"
          >
            <BookOpen className="w-4 h-4" />
          </button>
          <button
            onClick={() => setActiveSidebarTab('files')}
            className={`p-1.5 rounded-md transition-colors ${
              activeSidebarTab === 'files'
                ? 'bg-zinc-800 text-amber-400'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
            title="Файловый менеджер проекта"
          >
            <FolderTree className="w-4 h-4" />
          </button>
          <button
            onClick={() => setActiveSidebarTab('packages')}
            className={`relative p-1.5 rounded-md transition-colors ${
              activeSidebarTab === 'packages'
                ? 'bg-zinc-800 text-emerald-400'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
            title="Менеджер библиотек Pip"
          >
            <Package className="w-4 h-4" />
            {installedPackagesCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-emerald-500 text-[9px] font-bold text-zinc-950 flex items-center justify-center">
                {installedPackagesCount > 9 ? '9+' : installedPackagesCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
