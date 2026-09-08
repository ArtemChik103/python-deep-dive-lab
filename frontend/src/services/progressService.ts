import type {
  Achievement,
  Difficulty,
  LessonSolutionStats,
  ModuleItem,
  UserProgressOverview,
  UserProfile,
} from '../types';

const PROFILE_KEY = 'pydeep_user_profile';
const STATS_KEY = 'pydeep_lesson_stats_v2';
const ACHIEVEMENTS_KEY = 'pydeep_achievements_v2';
const RUN_COUNT_KEY = 'pydeep_run_count';

export const INITIAL_ACHIEVEMENTS: Achievement[] = [
  {
    id: 'first_run',
    title: 'Первый импульс',
    description: 'Выполнить первый скрипт в редакторе кода.',
    category: 'core',
    icon: 'Play',
    unlocked: false,
    progress: 0,
    requirementText: '1 запуск кода',
  },
  {
    id: 'first_lesson',
    title: 'Первая звезда',
    description: 'Успешно решить первое задание со 100% зеленых тестов.',
    category: 'core',
    icon: 'Sparkles',
    unlocked: false,
    progress: 0,
    requirementText: '1 пройденный урок',
  },
  {
    id: 'sharp_shooter',
    title: 'Снайпер 100%',
    description: 'Решить 3 разных урока с первой же попытки запуска тестов.',
    category: 'accuracy',
    icon: 'Target',
    unlocked: false,
    progress: 0,
    requirementText: '3 урока с 1 попытки',
  },
  {
    id: 'clean_mind',
    title: 'Чистый разум',
    description: 'Сдать урок без подсказок и без подглядывания в эталонное решение.',
    category: 'accuracy',
    icon: 'Brain',
    unlocked: false,
    progress: 0,
    requirementText: '1 урок без подсказок',
  },
  {
    id: 'module0_complete',
    title: 'Старт взят',
    description: 'Полностью завершить все задания Модуля 0 (Абсолютный старт).',
    category: 'core',
    icon: 'CheckCircle2',
    unlocked: false,
    progress: 0,
    requirementText: '4 урока Модуля 0',
  },
  {
    id: 'module1_complete',
    title: 'Арсенал питониста',
    description: 'Завершить все уроки Модуля 1 (Базовые инструменты).',
    category: 'core',
    icon: 'Award',
    unlocked: false,
    progress: 0,
    requirementText: '4 урока Модуля 1',
  },
  {
    id: 'speed_demon',
    title: 'Турбо-код',
    description: 'Пройти автотесты быстрее чем за 100 миллисекунд.',
    category: 'speed',
    icon: 'Zap',
    unlocked: false,
    progress: 0,
    requirementText: 'Тесты < 100 ms',
  },
  {
    id: 'plot_artist',
    title: 'Магия графиков',
    description: 'Построить и отобразить график в среде Matplotlib.',
    category: 'tools',
    icon: 'LineChart',
    unlocked: false,
    progress: 0,
    requirementText: '1 сгенерированный график',
  },
  {
    id: 'pip_master',
    title: 'Повелитель Pip',
    description: 'Установить и использовать сторонний пакет через Pip-менеджер.',
    category: 'tools',
    icon: 'Package',
    unlocked: false,
    progress: 0,
    requirementText: '1 установленный пакет',
  },
  {
    id: 'accuracy_elite',
    title: 'Идеальный код',
    description: 'Достичь 100% точности тестов на 5 или более уроках.',
    category: 'accuracy',
    icon: 'ShieldCheck',
    unlocked: false,
    progress: 0,
    requirementText: '5 уроков со 100% тестов',
  },
  {
    id: 'cpython_voyager',
    title: 'Инженер CPython',
    description: 'Решить задание из продвинутых модулей (ООП, Dunder, Asyncio или CPython).',
    category: 'internals',
    icon: 'Cpu',
    unlocked: false,
    progress: 0,
    requirementText: 'Урок из модулей 3-12',
  },
  {
    id: 'persistent_coder',
    title: 'Стальной характер',
    description: 'Исправить ошибки и успешно сдать задание после 3 и более попыток.',
    category: 'accuracy',
    icon: 'Flame',
    unlocked: false,
    progress: 0,
    requirementText: 'Успех после >= 3 попыток',
  },
];

export const getUserProfile = (): UserProfile => {
  try {
    const raw = localStorage.getItem(PROFILE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return {
    name: 'Pythonista',
    title: 'Исследователь глубин Python',
    avatarIcon: 'terminal',
    createdAt: new Date().toISOString(),
  };
};

export const saveUserProfile = (profile: UserProfile): void => {
  try {
    localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
  } catch {}
};

export const getLessonStatsMap = (): Record<string, LessonSolutionStats> => {
  try {
    const raw = localStorage.getItem(STATS_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return {};
};

export const saveLessonStatsMap = (statsMap: Record<string, LessonSolutionStats>): void => {
  try {
    localStorage.setItem(STATS_KEY, JSON.stringify(statsMap));
  } catch {}
};

export const getAchievements = (): Achievement[] => {
  try {
    const raw = localStorage.getItem(ACHIEVEMENTS_KEY);
    if (raw) {
      const stored: Achievement[] = JSON.parse(raw);
      return INITIAL_ACHIEVEMENTS.map((init) => {
        const found = stored.find((s) => s.id === init.id);
        return found ? { ...init, ...found } : init;
      });
    }
  } catch {}
  return INITIAL_ACHIEVEMENTS;
};

export const saveAchievements = (achievements: Achievement[]): void => {
  try {
    localStorage.setItem(ACHIEVEMENTS_KEY, JSON.stringify(achievements));
  } catch {}
};

export const getTotalRunCount = (): number => {
  try {
    const raw = localStorage.getItem(RUN_COUNT_KEY);
    return raw ? parseInt(raw, 10) || 0 : 0;
  } catch {
    return 0;
  }
};

export const incrementRunCount = (): number => {
  const current = getTotalRunCount() + 1;
  try {
    localStorage.setItem(RUN_COUNT_KEY, current.toString());
  } catch {}
  return current;
};

export interface RecordAttemptParams {
  lessonId: string;
  lessonTitle: string;
  moduleTitle: string;
  difficulty: Difficulty;
  passedCount: number;
  totalTests: number;
  allPassed: boolean;
  executionTimeMs: number;
  hintsUsed: number;
  solutionRevealed: boolean;
  solutionCopied?: boolean;
}

export const recordTestAttempt = (params: RecordAttemptParams): {
  updatedStats: Record<string, LessonSolutionStats>;
  updatedAchievements: Achievement[];
  newlyUnlocked: Achievement[];
} => {
  const statsMap = getLessonStatsMap();
  const existing = statsMap[params.lessonId];

  const attempts = (existing?.attemptsCount || 0) + 1;
  const bestPassed = Math.max(existing?.bestPassedCount || 0, params.passedCount);
  const totalTests = Math.max(existing?.totalTestsCount || 0, params.totalTests);
  const accuracy = totalTests > 0 ? Math.round((bestPassed / totalTests) * 100) : 0;
  const completed = Boolean(existing?.completed || params.allPassed);
  const solutionRevealed = Boolean(existing?.solutionRevealed || params.solutionRevealed);
  const solutionCopied = Boolean(existing?.solutionCopied || params.solutionCopied);
  const solvedIndependently = completed && !solutionRevealed;
  const bestTime = existing?.bestExecutionTimeMs
    ? Math.min(existing.bestExecutionTimeMs, params.executionTimeMs)
    : params.executionTimeMs;

  const currentStats: LessonSolutionStats = {
    lessonId: params.lessonId,
    moduleTitle: params.moduleTitle,
    lessonTitle: params.lessonTitle,
    difficulty: params.difficulty,
    completed,
    solvedIndependently,
    attemptsCount: attempts,
    bestPassedCount: bestPassed,
    totalTestsCount: totalTests,
    accuracyPercent: accuracy,
    bestExecutionTimeMs: bestTime,
    hintsUsedCount: Math.max(existing?.hintsUsedCount || 0, params.hintsUsed),
    solutionRevealed,
    solutionCopied,
    lastSolvedAt: params.allPassed ? new Date().toISOString() : existing?.lastSolvedAt,
  };

  statsMap[params.lessonId] = currentStats;
  saveLessonStatsMap(statsMap);

  const { updatedAchievements, newlyUnlocked } = evaluateAllAchievements(statsMap);
  saveAchievements(updatedAchievements);

  return {
    updatedStats: statsMap,
    updatedAchievements,
    newlyUnlocked,
  };
};

export const evaluateAllAchievements = (
  statsMap: Record<string, LessonSolutionStats>,
  extraContext?: { hasPlot?: boolean; hasPackage?: boolean }
): { updatedAchievements: Achievement[]; newlyUnlocked: Achievement[] } => {
  const currentAchievements = getAchievements();
  const newlyUnlocked: Achievement[] = [];
  const statsList = Object.values(statsMap);
  const totalRuns = getTotalRunCount();

  // Fair evaluations: achievements require solving INDEPENDENTLY (!s.solutionRevealed)
  const independentlySolved = statsList.filter((s) => s.completed && !s.solutionRevealed);
  const perfectFirstTry = statsList.filter(
    (s) => s.completed && !s.solutionRevealed && s.attemptsCount === 1 && s.accuracyPercent === 100
  );
  const perfectScoreCount = statsList.filter(
    (s) => s.completed && !s.solutionRevealed && s.accuracyPercent === 100
  ).length;
  const solvedNoHints = statsList.some(
    (s) => s.completed && !s.solutionRevealed && s.hintsUsedCount === 0
  );
  const solvedAfterStruggle = statsList.some(
    (s) => s.completed && !s.solutionRevealed && s.attemptsCount >= 3
  );
  const fastExecution = statsList.some(
    (s) => s.completed && !s.solutionRevealed && s.bestExecutionTimeMs > 0 && s.bestExecutionTimeMs < 100
  );

  const m0SolvedIndep = statsList.filter(
    (s) => s.lessonId.startsWith('m0_') && s.completed && !s.solutionRevealed
  ).length;
  const m1SolvedIndep = statsList.filter(
    (s) => s.lessonId.startsWith('m1_') && s.completed && !s.solutionRevealed
  ).length;
  const hasAdvancedSolvedIndep = statsList.some(
    (s) =>
      s.completed &&
      !s.solutionRevealed &&
      !s.lessonId.startsWith('m0_') &&
      !s.lessonId.startsWith('m1_') &&
      !s.lessonId.startsWith('m2_')
  );

  const updatedAchievements = currentAchievements.map((ach) => {
    if (ach.unlocked) return ach;

    let shouldUnlock = false;
    let progress = ach.progress;

    switch (ach.id) {
      case 'first_run':
        progress = totalRuns > 0 ? 100 : 0;
        shouldUnlock = totalRuns > 0;
        break;

      case 'first_lesson':
        progress = independentlySolved.length > 0 ? 100 : 0;
        shouldUnlock = independentlySolved.length > 0;
        break;

      case 'sharp_shooter':
        progress = Math.min(100, Math.round((perfectFirstTry.length / 3) * 100));
        shouldUnlock = perfectFirstTry.length >= 3;
        break;

      case 'clean_mind':
        progress = solvedNoHints ? 100 : 0;
        shouldUnlock = solvedNoHints;
        break;

      case 'module0_complete':
        progress = Math.min(100, Math.round((m0SolvedIndep / 4) * 100));
        shouldUnlock = m0SolvedIndep >= 4;
        break;

      case 'module1_complete':
        progress = Math.min(100, Math.round((m1SolvedIndep / 4) * 100));
        shouldUnlock = m1SolvedIndep >= 4;
        break;

      case 'speed_demon':
        progress = fastExecution ? 100 : 0;
        shouldUnlock = fastExecution;
        break;

      case 'plot_artist':
        if (extraContext?.hasPlot) {
          progress = 100;
          shouldUnlock = true;
        }
        break;

      case 'pip_master':
        if (extraContext?.hasPackage) {
          progress = 100;
          shouldUnlock = true;
        }
        break;

      case 'accuracy_elite':
        progress = Math.min(100, Math.round((perfectScoreCount / 5) * 100));
        shouldUnlock = perfectScoreCount >= 5;
        break;

      case 'cpython_voyager':
        progress = hasAdvancedSolvedIndep ? 100 : 0;
        shouldUnlock = hasAdvancedSolvedIndep;
        break;

      case 'persistent_coder':
        progress = solvedAfterStruggle ? 100 : 0;
        shouldUnlock = solvedAfterStruggle;
        break;
    }

    if (shouldUnlock && !ach.unlocked) {
      const unlockedItem = {
        ...ach,
        unlocked: true,
        progress: 100,
        unlockedAt: new Date().toISOString(),
      };
      newlyUnlocked.push(unlockedItem);
      return unlockedItem;
    }

    return { ...ach, progress };
  });

  return { updatedAchievements, newlyUnlocked };
};

export const computeOverview = (
  modules: ModuleItem[],
  statsMap: Record<string, LessonSolutionStats>,
  achievements: Achievement[]
): UserProgressOverview => {
  const totalLessons = modules.reduce((acc, m) => acc + m.lessons.length, 0);
  const statsList = Object.values(statsMap);

  const completedLessons = statsList.filter((s) => s.completed).length;
  const independentLessonsCount = statsList.filter((s) => s.completed && !s.solutionRevealed).length;
  const revealedLessonsCount = statsList.filter((s) => s.completed && s.solutionRevealed).length;

  let totalTestsRun = 0;
  let totalTestsPassed = 0;
  let cleanTestsRun = 0;
  let cleanTestsPassed = 0;
  let totalTimeMs = 0;
  let timedLessonsCount = 0;

  statsList.forEach((s) => {
    totalTestsRun += s.totalTestsCount;
    totalTestsPassed += s.bestPassedCount;
    if (!s.solutionRevealed) {
      cleanTestsRun += s.totalTestsCount;
      cleanTestsPassed += s.bestPassedCount;
    }
    if (s.bestExecutionTimeMs > 0) {
      totalTimeMs += s.bestExecutionTimeMs;
      timedLessonsCount++;
    }
  });

  const overallAccuracy =
    totalTestsRun > 0 ? Math.round((totalTestsPassed / totalTestsRun) * 100) : 0;

  const cleanAccuracy =
    cleanTestsRun > 0
      ? Math.round((cleanTestsPassed / cleanTestsRun) * 100)
      : independentLessonsCount > 0
      ? overallAccuracy
      : overallAccuracy;

  const averageExecutionTimeMs =
    timedLessonsCount > 0 ? Math.round(totalTimeMs / timedLessonsCount) : 0;

  const unlockedAchievementsCount = achievements.filter((a) => a.unlocked).length;

  // Fair XP formula:
  // 100 XP for each independently solved lesson
  // 15 XP for reference solution inspection (audit/study mode)
  // 150 XP per unlocked achievement
  // Accuracy bonus
  const xp =
    independentLessonsCount * 100 +
    revealedLessonsCount * 15 +
    unlockedAchievementsCount * 150 +
    Math.round(cleanAccuracy * 2);

  let level = 1;
  let levelTitle = 'Новичок в Python';
  let nextLevelXp = 300;

  if (xp >= 3000) {
    level = 5;
    levelTitle = 'Архитектор CPython';
    nextLevelXp = 5000;
  } else if (xp >= 1600) {
    level = 4;
    levelTitle = 'Сеньор-инженер';
    nextLevelXp = 3000;
  } else if (xp >= 800) {
    level = 3;
    levelTitle = 'Мидл-разработчик';
    nextLevelXp = 1600;
  } else if (xp >= 300) {
    level = 2;
    levelTitle = 'Джуниор-программист';
    nextLevelXp = 800;
  }

  return {
    totalLessons: totalLessons || 30,
    completedLessons,
    independentLessonsCount,
    revealedLessonsCount,
    totalTestsRun,
    totalTestsPassed,
    overallAccuracy,
    cleanAccuracy,
    totalCodeRuns: getTotalRunCount(),
    averageExecutionTimeMs,
    unlockedAchievementsCount,
    totalAchievementsCount: achievements.length,
    level,
    levelTitle,
    xp,
    nextLevelXp,
  };
};
