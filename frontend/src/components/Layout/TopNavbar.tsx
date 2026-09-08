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
  Menu,
  FileCode2,
  Terminal,
  User,
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
  // Profile props
  userLevel?: number;
  userAccuracy?: number;
  onOpenProfile?: () => void;
  // Mobile props
  isMobile: boolean;
  mobileActiveView: 'theory' | 'editor' | 'console';
  setMobileActiveView: (view: 'theory' | 'editor' | 'console') => void;
  onToggleMobileSidebar: () => void;
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
  userLevel,
  userAccuracy,
  onOpenProfile,
  isMobile,
  mobileActiveView,
  setMobileActiveView,
  onToggleMobileSidebar,
}) => {
  const progressPercent = totalLessons > 0 ? Math.round((completedCount / totalLessons) * 100) : 0;

  return (
    <header className="bg-zinc-900 border-b border-zinc-800 flex flex-col shrink-0 z-30 select-none">
      {/* Top Main Row */}
      <div className="h-14 flex items-center justify-between px-3 md:px-4 gap-2">
        {/* Left: Mobile Menu Trigger + Brand */}
        <div className="flex items-center gap-2 md:gap-4 min-w-0">
          {/* Hamburger button for mobile */}
          <button
            onClick={onToggleMobileSidebar}
            className="md:hidden p-2 text-zinc-300 hover:text-white hover:bg-zinc-800 rounded-lg transition-colors cursor-pointer"
            title="Открыть меню"
            aria-label="Открыть меню"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2 shrink-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center shadow-sm">
              <span className="text-white font-black text-sm tracking-tighter">Py</span>
            </div>
            <div>
              <span className="sr-only">Python Deep Dive</span>
              <span className="font-bold text-xs sm:text-sm text-zinc-100 tracking-tight">PyDeep</span>
              <span className="hidden sm:inline font-bold text-sm text-zinc-100 tracking-tight"> Dive</span>
              <span className="ml-1.5 text-[10px] sm:text-xs px-1.5 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800 font-mono font-medium hidden xs:inline">
                v1.0
              </span>
            </div>
          </div>

          {/* Mode Switcher (Desktop only; on mobile accessible via drawer) */}
          <div className="hidden md:flex items-center bg-zinc-950 p-1 rounded-lg border border-zinc-800">
            <button
              onClick={() => {
                setMode('curriculum');
                setActiveSidebarTab('curriculum');
                if (isMobile) setMobileActiveView('theory');
              }}
              className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md transition-colors cursor-pointer ${
                mode === 'curriculum'
                  ? 'bg-zinc-800 text-zinc-100 shadow-xs'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 text-sky-400" />
              <span className="hidden xs:inline">Обучение</span>
            </button>
            <button
              onClick={() => {
                setMode('sandbox');
                setActiveSidebarTab('files');
                if (isMobile) setMobileActiveView('editor');
              }}
              className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md transition-colors cursor-pointer ${
                mode === 'sandbox'
                  ? 'bg-zinc-800 text-zinc-100 shadow-xs'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <FlaskConical className="w-3.5 h-3.5 text-emerald-400" />
              <span className="hidden xs:inline">Песочница</span>
            </button>
          </div>
        </div>

        {/* Center/Right: Action Buttons */}
        <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
          <button
            onClick={onRunCode}
            disabled={isRunning || isTesting}
            className="flex items-center gap-1.5 px-2.5 sm:px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 active:bg-emerald-700 disabled:opacity-50 text-white text-xs font-semibold rounded-md shadow-xs transition-colors cursor-pointer"
            title="Запустить код"
          >
            <Play className={`w-3.5 h-3.5 fill-current ${isRunning ? 'animate-spin' : ''}`} />
            <span>{isRunning ? '...' : 'Запустить'}</span>
          </button>

          {mode === 'curriculum' && (
            <button
              onClick={onRunTests}
              disabled={isRunning || isTesting}
              className="flex items-center gap-1.5 px-2.5 sm:px-3.5 py-1.5 bg-sky-600 hover:bg-sky-500 active:bg-sky-700 disabled:opacity-50 text-white text-xs font-semibold rounded-md shadow-xs transition-colors cursor-pointer"
              title="Проверить тесты"
            >
              <CheckCircle2 className={`w-3.5 h-3.5 ${isTesting ? 'animate-spin' : ''}`} />
              <span className="hidden sm:inline">{isTesting ? 'Проверка...' : 'Проверить тесты'}</span>
              <span className="sm:hidden">{isTesting ? '...' : 'Тесты'}</span>
            </button>
          )}

          <button
            onClick={onResetCode}
            className="p-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded-md transition-colors hidden sm:block"
            title="Сбросить код к исходному"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          {/* Desktop Right Sidebars buttons */}
          <div className="hidden md:flex items-center gap-3 ml-2">
            {mode === 'curriculum' && (
              <div className="flex items-center gap-2 px-2.5 py-1 rounded-md bg-zinc-950 border border-zinc-800">
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

            <div className="flex items-center bg-zinc-950 p-0.5 rounded-lg border border-zinc-800">
              <button
                onClick={() => setActiveSidebarTab('curriculum')}
                className={`p-1.5 rounded-md transition-colors cursor-pointer ${
                  activeSidebarTab === 'curriculum' ? 'bg-zinc-800 text-sky-400' : 'text-zinc-400 hover:text-zinc-200'
                }`}
                title="Программа курса"
              >
                <BookOpen className="w-4 h-4" />
              </button>
              <button
                onClick={() => setActiveSidebarTab('files')}
                className={`p-1.5 rounded-md transition-colors cursor-pointer ${
                  activeSidebarTab === 'files' ? 'bg-zinc-800 text-amber-400' : 'text-zinc-400 hover:text-zinc-200'
                }`}
                title="Файловый менеджер проекта"
              >
                <FolderTree className="w-4 h-4" />
              </button>
              <button
                onClick={() => setActiveSidebarTab('packages')}
                className={`relative p-1.5 rounded-md transition-colors cursor-pointer ${
                  activeSidebarTab === 'packages' ? 'bg-zinc-800 text-emerald-400' : 'text-zinc-400 hover:text-zinc-200'
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
            {onOpenProfile && (
              <button
                onClick={onOpenProfile}
                className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-zinc-950 border border-zinc-800 hover:border-sky-700/60 hover:bg-zinc-850 transition-colors cursor-pointer text-zinc-300 hover:text-white ml-1"
                title="Профиль пользователя и достижения"
              >
                <div className="w-5 h-5 rounded-full bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center text-[10px] font-bold text-white shadow-xs">
                  {userLevel || 1}
                </div>
                <div className="flex flex-col text-left">
                  <span className="text-[10px] text-zinc-400 font-medium leading-none">Профиль</span>
                  <span className="text-[11px] font-bold text-sky-400 leading-tight">
                    {userAccuracy !== undefined ? `${userAccuracy}% точн.` : 'Ачивки'}
                  </span>
                </div>
              </button>
            )}
          </div>

          {/* Mobile Profile Button */}
          {onOpenProfile && (
            <button
              onClick={onOpenProfile}
              className="md:hidden p-1.5 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-md transition-colors cursor-pointer relative"
              title="Профиль и достижения"
            >
              <User className="w-4 h-4 text-sky-400" />
              <span className="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-sky-500 text-[9px] font-bold text-zinc-950 flex items-center justify-center">
                {userLevel || 1}
              </span>
            </button>
          )}
        </div>
      </div>

      {/* Mobile View Switcher (Only visible on mobile screens < 768px) */}
      {isMobile && (
        <div className="md:hidden flex items-center bg-zinc-950 border-t border-zinc-800 p-1 gap-1">
          {mode === 'curriculum' && (
            <button
              onClick={() => setMobileActiveView('theory')}
              className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-1 text-xs font-medium rounded-md transition-colors cursor-pointer text-center ${
                mobileActiveView === 'theory'
                  ? 'bg-sky-950 text-sky-400 border border-sky-800 font-semibold shadow-xs'
                  : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 shrink-0" />
              <span>Теория<span className="hidden xs:inline"> & Задание</span></span>
            </button>
          )}

          <button
            onClick={() => setMobileActiveView('editor')}
            className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-1 text-xs font-medium rounded-md transition-colors cursor-pointer text-center ${
              mobileActiveView === 'editor'
                ? 'bg-zinc-800 text-zinc-100 border border-zinc-700 font-semibold shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900'
            }`}
          >
            <FileCode2 className="w-3.5 h-3.5 shrink-0 text-sky-400" />
            <span>Редактор<span className="hidden xs:inline"> кода</span></span>
          </button>

          <button
            onClick={() => setMobileActiveView('console')}
            className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-1 text-xs font-medium rounded-md transition-colors cursor-pointer text-center ${
              mobileActiveView === 'console'
                ? 'bg-zinc-800 text-emerald-400 border border-zinc-700 font-semibold shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900'
            }`}
          >
            <Terminal className="w-3.5 h-3.5 shrink-0" />
            <span>Консоль<span className="hidden xs:inline"> / Тесты</span></span>
          </button>
        </div>
      )}
    </header>
  );
};
