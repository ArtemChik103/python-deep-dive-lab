import React, { useState } from 'react';
import {
  X,
  Trophy,
  Target,
  CheckCircle2,
  Clock,
  Zap,
  Play,
  Sparkles,
  Award,
  Brain,
  ShieldCheck,
  Cpu,
  Flame,
  LineChart,
  Package,
  Lock,
  Search,
  RotateCcw,
  Edit2,
  Check,
  User,
  Activity,
  AlertCircle,
} from 'lucide-react';
import type {
  Achievement,
  LessonSolutionStats,
  ModuleItem,
  UserProgressOverview,
  UserProfile,
} from '../../types';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: UserProfile;
  onUpdateProfile: (updated: UserProfile) => void;
  overview: UserProgressOverview;
  statsMap: Record<string, LessonSolutionStats>;
  achievements: Achievement[];
  modules: ModuleItem[];
  onSelectLesson?: (lessonId: string) => void;
  onResetProgress?: () => void;
}

const ICON_MAP: Record<string, React.ElementType> = {
  Play,
  Sparkles,
  Target,
  Brain,
  CheckCircle2,
  Award,
  Zap,
  LineChart,
  Package,
  ShieldCheck,
  Cpu,
  Flame,
};

export const ProfileModal: React.FC<ProfileModalProps> = ({
  isOpen,
  onClose,
  profile,
  onUpdateProfile,
  overview,
  statsMap,
  achievements,
  modules,
  onSelectLesson,
  onResetProgress,
}) => {
  const [activeTab, setActiveTab] = useState<'accuracy' | 'achievements' | 'settings'>('accuracy');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [isEditingName, setIsEditingName] = useState(false);
  const [nameInput, setNameInput] = useState(profile.name);
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  React.useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSaveName = () => {
    if (nameInput.trim()) {
      onUpdateProfile({ ...profile, name: nameInput.trim() });
    }
    setIsEditingName(false);
  };

  // Compile all lessons with stats
  const allLessons = modules.flatMap((m) =>
    m.lessons.map((l) => {
      const stat = statsMap[l.id];
      return {
        lessonId: l.id,
        lessonTitle: l.title,
        moduleTitle: m.title,
        difficulty: l.difficulty,
        stat,
      };
    })
  );

  const filteredLessons = allLessons.filter((item) => {
    const matchesSearch =
      item.lessonTitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.moduleTitle.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;

    if (filterCategory === 'completed') return item.stat?.completed;
    if (filterCategory === 'in_progress') return item.stat && !item.stat.completed;
    if (filterCategory === 'unsolved') return !item.stat;
    return true;
  });

  const xpProgressPercent = Math.min(
    100,
    Math.round((overview.xp / overview.nextLevelXp) * 100)
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 animate-in fade-in duration-200">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal Dialog */}
      <div className="relative w-full max-w-3xl max-h-[90vh] bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl flex flex-col z-10 overflow-hidden text-zinc-100">
        {/* Modal Header & User Hero */}
        <div className="p-4 sm:p-5 bg-gradient-to-r from-zinc-950 via-zinc-900 to-sky-950/40 border-b border-zinc-800 shrink-0">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center gap-3.5">
              {/* Avatar Icon */}
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20 shrink-0">
                <User className="w-6 h-6 text-white" />
              </div>

              <div>
                <div className="flex items-center gap-2">
                  {isEditingName ? (
                    <div className="flex items-center gap-1">
                      <input
                        type="text"
                        value={nameInput}
                        onChange={(e) => setNameInput(e.target.value)}
                        className="px-2 py-0.5 bg-zinc-800 border border-sky-500 rounded text-sm text-white focus:outline-none"
                        autoFocus
                      />
                      <button
                        onClick={handleSaveName}
                        className="p-1 text-emerald-400 hover:text-emerald-300 cursor-pointer"
                      >
                        <Check className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1.5">
                      <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">
                        {profile.name}
                      </h2>
                      <button
                        onClick={() => {
                          setNameInput(profile.name);
                          setIsEditingName(true);
                        }}
                        className="p-1 text-zinc-500 hover:text-zinc-300 cursor-pointer"
                        title="Изменить имя"
                      >
                        <Edit2 className="w-3 h-3" />
                      </button>
                    </div>
                  )}

                  <span className="px-2 py-0.5 rounded-full bg-sky-950 border border-sky-800 text-[10px] font-bold text-sky-300">
                    LVL {overview.level}
                  </span>
                </div>

                <p className="text-xs text-zinc-400 font-medium">{overview.levelTitle}</p>

                {/* XP Bar */}
                <div className="flex items-center gap-2 mt-1.5">
                  <div className="w-32 sm:w-44 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-sky-500 to-emerald-400 rounded-full transition-all duration-500"
                      style={{ width: `${xpProgressPercent}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-zinc-400 font-mono">
                    {overview.xp} / {overview.nextLevelXp} XP
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800 transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Quick Stat Highlights */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-4">
            <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-2.5 flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-md bg-emerald-950/60 border border-emerald-800/60 flex items-center justify-center shrink-0">
                <Target className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <div className="text-[10px] text-zinc-400">Точность тестов</div>
                <div className="text-sm font-bold text-emerald-400 font-mono">
                  {overview.overallAccuracy}%
                </div>
              </div>
            </div>

            <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-2.5 flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-md bg-sky-950/60 border border-sky-800/60 flex items-center justify-center shrink-0">
                <CheckCircle2 className="w-4 h-4 text-sky-400" />
              </div>
              <div>
                <div className="text-[10px] text-zinc-400">Тестов пройдено</div>
                <div className="text-sm font-bold text-sky-400 font-mono">
                  {overview.totalTestsPassed} / {overview.totalTestsRun}
                </div>
              </div>
            </div>

            <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-2.5 flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-md bg-amber-950/60 border border-amber-800/60 flex items-center justify-center shrink-0">
                <Trophy className="w-4 h-4 text-amber-400" />
              </div>
              <div>
                <div className="text-[10px] text-zinc-400">Достижения</div>
                <div className="text-sm font-bold text-amber-400 font-mono">
                  {overview.unlockedAchievementsCount} / {overview.totalAchievementsCount}
                </div>
              </div>
            </div>

            <div className="bg-zinc-950/70 border border-zinc-800/80 rounded-lg p-2.5 flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-md bg-indigo-950/60 border border-indigo-800/60 flex items-center justify-center shrink-0">
                <Clock className="w-4 h-4 text-indigo-400" />
              </div>
              <div>
                <div className="text-[10px] text-zinc-400">Ср. время тестов</div>
                <div className="text-sm font-bold text-indigo-300 font-mono">
                  ~{overview.averageExecutionTimeMs} ms
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="h-10 bg-zinc-950 border-b border-zinc-800 flex items-center px-4 gap-2 shrink-0">
          <button
            onClick={() => setActiveTab('accuracy')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-md font-medium transition-colors cursor-pointer ${
              activeTab === 'accuracy'
                ? 'bg-zinc-800 text-sky-400 font-semibold shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            <span>Точность решений & Тесты</span>
          </button>

          <button
            onClick={() => setActiveTab('achievements')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-md font-medium transition-colors cursor-pointer ${
              activeTab === 'achievements'
                ? 'bg-zinc-800 text-amber-400 font-semibold shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Trophy className="w-3.5 h-3.5" />
            <span>Ачивки ({overview.unlockedAchievementsCount})</span>
          </button>

          <button
            onClick={() => setActiveTab('settings')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-md font-medium transition-colors cursor-pointer ${
              activeTab === 'settings'
                ? 'bg-zinc-800 text-zinc-200 font-semibold shadow-xs'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Управление данными</span>
          </button>
        </div>

        {/* Tab Body */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
          {/* TAB 1: ACCURACY & DETAILED LESSON TESTS */}
          {activeTab === 'accuracy' && (
            <div className="space-y-4">
              {/* Search and Filters */}
              <div className="flex flex-wrap items-center justify-between gap-2.5">
                <div className="relative flex-1 min-w-[200px]">
                  <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Поиск по урокам и модулям..."
                    className="w-full pl-8 pr-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-md text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-sky-500"
                  />
                </div>

                <div className="flex items-center gap-1 text-xs">
                  <button
                    onClick={() => setFilterCategory('all')}
                    className={`px-2.5 py-1 rounded-md transition-colors cursor-pointer ${
                      filterCategory === 'all'
                        ? 'bg-zinc-800 text-white font-medium'
                        : 'text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    Все ({allLessons.length})
                  </button>
                  <button
                    onClick={() => setFilterCategory('completed')}
                    className={`px-2.5 py-1 rounded-md transition-colors cursor-pointer ${
                      filterCategory === 'completed'
                        ? 'bg-emerald-950 text-emerald-300 border border-emerald-800 font-medium'
                        : 'text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    Решено ({overview.completedLessons})
                  </button>
                  <button
                    onClick={() => setFilterCategory('in_progress')}
                    className={`px-2.5 py-1 rounded-md transition-colors cursor-pointer ${
                      filterCategory === 'in_progress'
                        ? 'bg-amber-950 text-amber-300 border border-amber-800 font-medium'
                        : 'text-zinc-400 hover:text-zinc-200'
                    }`}
                  >
                    В процессе
                  </button>
                </div>
              </div>

              {/* Lesson Accuracy List */}
              <div className="space-y-2">
                {filteredLessons.length === 0 ? (
                  <div className="text-center py-8 text-zinc-500 text-xs">
                    Уроков по данному фильтру не найдено
                  </div>
                ) : (
                  filteredLessons.map((item) => {
                    const hasStat = Boolean(item.stat);
                    const accuracy = item.stat?.accuracyPercent || 0;
                    const passed = item.stat?.bestPassedCount || 0;
                    const total = item.stat?.totalTestsCount || 0;

                    return (
                      <div
                        key={item.lessonId}
                        className={`p-3 rounded-lg border transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                          item.stat?.completed
                            ? 'bg-zinc-950/80 border-emerald-900/40 hover:border-emerald-700/60'
                            : hasStat
                            ? 'bg-zinc-950/80 border-amber-900/40 hover:border-amber-700/60'
                            : 'bg-zinc-950/40 border-zinc-850 opacity-70'
                        }`}
                      >
                        <div className="space-y-1">
                          <div className="text-[10px] text-zinc-400">{item.moduleTitle}</div>
                          <div className="text-xs font-semibold text-zinc-100">
                            {item.lessonTitle}
                          </div>
                          <div className="flex flex-wrap items-center gap-2 pt-0.5 text-[10px] text-zinc-400">
                            <span className="capitalize px-1.5 py-0.2 rounded bg-zinc-850 text-zinc-300 font-mono">
                              {item.difficulty}
                            </span>
                            {hasStat && (
                              <>
                                <span>Попыток: {item.stat?.attemptsCount}</span>
                                <span>•</span>
                                <span>Подсказок: {item.stat?.hintsUsedCount}</span>
                                {item.stat?.bestExecutionTimeMs ? (
                                  <>
                                    <span>•</span>
                                    <span>{item.stat.bestExecutionTimeMs} ms</span>
                                  </>
                                ) : null}
                              </>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center gap-3 shrink-0 self-end sm:self-center">
                          {/* Accuracy Badge */}
                          {hasStat ? (
                            <div className="text-right">
                              <div
                                className={`text-xs font-bold font-mono px-2 py-0.5 rounded-md inline-block ${
                                  accuracy === 100
                                    ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                                    : accuracy >= 50
                                    ? 'bg-amber-950 text-amber-300 border border-amber-800'
                                    : 'bg-rose-950 text-rose-300 border border-rose-800'
                                }`}
                              >
                                {accuracy}% ({passed}/{total} тестов)
                              </div>
                              <div className="text-[9px] text-zinc-500 mt-0.5">
                                {item.stat?.completed ? 'Все тесты пройдены' : 'Частичный успех'}
                              </div>
                            </div>
                          ) : (
                            <span className="text-[11px] text-zinc-500 italic">
                              Еще не запускалось
                            </span>
                          )}

                          {onSelectLesson && (
                            <button
                              onClick={() => {
                                onSelectLesson(item.lessonId);
                                onClose();
                              }}
                              className="px-2.5 py-1 text-xs font-medium rounded bg-zinc-800 hover:bg-sky-600 hover:text-white text-zinc-300 transition-colors cursor-pointer"
                            >
                              Открыть →
                            </button>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          )}

          {/* TAB 2: ACHIEVEMENTS */}
          {activeTab === 'achievements' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {achievements.map((ach) => {
                  const IconComp = ICON_MAP[ach.icon] || Trophy;

                  return (
                    <div
                      key={ach.id}
                      className={`p-3.5 rounded-lg border transition-all relative overflow-hidden flex gap-3.5 ${
                        ach.unlocked
                          ? 'bg-gradient-to-br from-zinc-900 to-zinc-950 border-amber-600/50 shadow-md shadow-amber-950/20'
                          : 'bg-zinc-950/50 border-zinc-850 opacity-60'
                      }`}
                    >
                      <div
                        className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                          ach.unlocked
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            : 'bg-zinc-900 text-zinc-600 border border-zinc-800'
                        }`}
                      >
                        {ach.unlocked ? (
                          <IconComp className="w-5 h-5" />
                        ) : (
                          <Lock className="w-4 h-4" />
                        )}
                      </div>

                      <div className="flex-1 min-w-0 space-y-1">
                        <div className="flex items-center justify-between gap-1">
                          <h4
                            className={`text-xs font-bold truncate ${
                              ach.unlocked ? 'text-amber-300' : 'text-zinc-400'
                            }`}
                          >
                            {ach.title}
                          </h4>
                          {ach.unlocked ? (
                            <span className="text-[9px] font-semibold text-emerald-400 bg-emerald-950/80 px-1.5 py-0.2 rounded border border-emerald-800">
                              Открыто
                            </span>
                          ) : (
                            <span className="text-[9px] text-zinc-500 font-mono">
                              {ach.progress}%
                            </span>
                          )}
                        </div>

                        <p className="text-[11px] text-zinc-400 leading-snug">
                          {ach.description}
                        </p>

                        {!ach.unlocked && (
                          <div className="pt-1">
                            <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-amber-500/70 rounded-full transition-all duration-300"
                                style={{ width: `${ach.progress}%` }}
                              />
                            </div>
                            <div className="text-[9px] text-zinc-500 mt-1">
                              Условие: {ach.requirementText}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 3: SETTINGS & DATA MANAGEMENT */}
          {activeTab === 'settings' && (
            <div className="space-y-4 text-xs">
              <div className="p-4 rounded-lg bg-zinc-950 border border-zinc-800 space-y-3">
                <h3 className="font-semibold text-zinc-200">Имя пользователя</h3>
                <div className="flex items-center gap-2 max-w-sm">
                  <input
                    type="text"
                    value={nameInput}
                    onChange={(e) => setNameInput(e.target.value)}
                    className="flex-1 px-3 py-1.5 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:outline-none focus:border-sky-500"
                  />
                  <button
                    onClick={handleSaveName}
                    className="px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white rounded font-medium cursor-pointer"
                  >
                    Сохранить
                  </button>
                </div>
              </div>

              <div className="p-4 rounded-lg bg-zinc-950 border border-zinc-800 space-y-3">
                <h3 className="font-semibold text-zinc-200">Экспорт данных</h3>
                <p className="text-zinc-400 leading-relaxed">
                  Вы можете экспортировать свои решения, историю прохождения тестов и достижения в JSON-файл для резервного сохранения.
                </p>
                <button
                  onClick={() => {
                    const data = {
                      profile,
                      overview,
                      statsMap,
                      achievements,
                      exportedAt: new Date().toISOString(),
                    };
                    const blob = new Blob([JSON.stringify(data, null, 2)], {
                      type: 'application/json',
                    });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `pydeep_progress_${new Date().toISOString().split('T')[0]}.json`;
                    a.click();
                    URL.revokeObjectURL(url);
                  }}
                  className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded font-medium cursor-pointer"
                >
                  Скачать JSON с прогрессом
                </button>
              </div>

              <div className="p-4 rounded-lg bg-rose-950/20 border border-rose-900/40 space-y-3">
                <div className="flex items-center gap-2 text-rose-400 font-semibold">
                  <AlertCircle className="w-4 h-4" />
                  <span>Сброс прогресса</span>
                </div>
                <p className="text-rose-200/80 leading-relaxed">
                  Это действие удалит локальную статистику прохождения уроков, историю запусков и сбросит открытые достижения.
                </p>

                {showResetConfirm ? (
                  <div className="flex items-center gap-2 pt-1">
                    <button
                      onClick={() => {
                        if (onResetProgress) onResetProgress();
                        setShowResetConfirm(false);
                      }}
                      className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded font-medium cursor-pointer"
                    >
                      Да, сбросить всё
                    </button>
                    <button
                      onClick={() => setShowResetConfirm(false)}
                      className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-medium cursor-pointer"
                    >
                      Отмена
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowResetConfirm(true)}
                    className="px-3 py-1.5 bg-rose-950/50 hover:bg-rose-900/60 border border-rose-800/60 text-rose-300 rounded font-medium cursor-pointer"
                  >
                    Сбросить статистику и ачивки...
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
