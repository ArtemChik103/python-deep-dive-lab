import React, { useState } from 'react';
import {
  Search,
  CheckCircle2,
  Circle,
  ChevronDown,
  ChevronRight,
  Clock,
  HelpCircle,
  Award,
} from 'lucide-react';
import type { Difficulty, ModuleItem } from '../../types';

interface CurriculumTreeProps {
  modules: ModuleItem[];
  selectedLessonId: string | null;
  onSelectLesson: (lessonId: string) => void;
  completedLessonIds: Set<string>;
}

export const CurriculumTree: React.FC<CurriculumTreeProps> = ({
  modules,
  selectedLessonId,
  onSelectLesson,
  completedLessonIds,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty | 'all'>('all');
  const [expandedModules, setExpandedModules] = useState<Record<string, boolean>>(() => {
    return {
      module_1: true,
      module_2: true,
    };
  });

  const toggleModule = (modId: string) => {
    setExpandedModules((prev) => ({
      ...prev,
      [modId]: !prev[modId],
    }));
  };

  const getDifficultyBadge = (diff: Difficulty) => {
    switch (diff) {
      case 'beginner':
        return <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 font-medium">Легкий</span>;
      case 'intermediate':
        return <span className="text-[10px] px-1.5 py-0.5 rounded bg-sky-950/80 text-sky-400 border border-sky-800/60 font-medium">Средний</span>;
      case 'advanced':
        return <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800/60 font-medium">Сложный</span>;
      case 'expert':
        return <span className="text-[10px] px-1.5 py-0.5 rounded bg-rose-950/80 text-rose-400 border border-rose-800/60 font-medium">Эксперт</span>;
    }
  };

  const filteredModules = modules.map((mod) => {
    const matchingLessons = mod.lessons.filter((l) => {
      const matchesSearch =
        searchQuery.trim() === '' ||
        l.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        mod.title.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesDiff = selectedDifficulty === 'all' || l.difficulty === selectedDifficulty;
      return matchesSearch && matchesDiff;
    });

    return {
      ...mod,
      lessons: matchingLessons,
    };
  }).filter((mod) => mod.lessons.length > 0);

  return (
    <div className="flex flex-col h-full bg-zinc-900 border-r border-zinc-800 select-none overflow-hidden">
      {/* Header & Search */}
      <div className="p-3 border-b border-zinc-800 shrink-0 space-y-2.5">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-zinc-300 uppercase tracking-wider">
            Программа обучения
          </span>
          <span className="text-xs text-zinc-400 font-mono">
            {completedLessonIds.size} решено
          </span>
        </div>

        {/* Search Input */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-zinc-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Поиск тем, CPython, async..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-md text-xs text-zinc-200 placeholder-zinc-500 focus:outline-hidden focus:border-sky-500 transition-colors"
          />
        </div>

        {/* Difficulty Filter Pills */}
        <div className="flex items-center gap-1 overflow-x-auto pb-0.5 text-[11px]">
          {(['all', 'beginner', 'intermediate', 'advanced', 'expert'] as const).map((diff) => (
            <button
              key={diff}
              onClick={() => setSelectedDifficulty(diff)}
              className={`px-2 py-0.5 rounded-sm transition-colors whitespace-nowrap ${
                selectedDifficulty === diff
                  ? 'bg-zinc-800 text-zinc-100 font-medium'
                  : 'text-zinc-400 hover:text-zinc-300'
              }`}
            >
              {diff === 'all'
                ? 'Все'
                : diff === 'beginner'
                ? 'База'
                : diff === 'intermediate'
                ? 'Мидл'
                : diff === 'advanced'
                ? 'Сложно'
                : 'Эксперт'}
            </button>
          ))}
        </div>
      </div>

      {/* Modules List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
        {filteredModules.length === 0 ? (
          <div className="p-4 text-center text-xs text-zinc-400">
            Ничего не найдено по заданному фильтру
          </div>
        ) : (
          filteredModules.map((mod) => {
            const isExpanded = expandedModules[mod.id] ?? true;
            const completedInMod = mod.lessons.filter((l) => completedLessonIds.has(l.id)).length;
            const allCompleted = mod.lessons.length > 0 && completedInMod === mod.lessons.length;

            return (
              <div key={mod.id} className="rounded-lg bg-zinc-950/60 border border-zinc-800/80 overflow-hidden">
                {/* Module Header */}
                <button
                  onClick={() => toggleModule(mod.id)}
                  className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-zinc-800/40 transition-colors"
                >
                  <div className="flex items-center gap-2 min-w-0 pr-2">
                    {isExpanded ? (
                      <ChevronDown className="w-3.5 h-3.5 text-zinc-400 shrink-0" />
                    ) : (
                      <ChevronRight className="w-3.5 h-3.5 text-zinc-400 shrink-0" />
                    )}
                    <span className="text-xs font-semibold text-zinc-200 truncate">
                      {mod.title}
                    </span>
                  </div>

                  <div className="flex items-center gap-1.5 shrink-0">
                    {allCompleted ? (
                      <Award className="w-3.5 h-3.5 text-amber-400" />
                    ) : (
                      <span className="text-[10px] text-zinc-400 font-mono">
                        {completedInMod}/{mod.lessons.length}
                      </span>
                    )}
                  </div>
                </button>

                {/* Lessons in Module */}
                {isExpanded && (
                  <div className="border-t border-zinc-800/60 divide-y divide-zinc-800/40">
                    {mod.lessons.map((lesson) => {
                      const isSelected = lesson.id === selectedLessonId;
                      const isCompleted = completedLessonIds.has(lesson.id);

                      return (
                        <button
                          key={lesson.id}
                          onClick={() => onSelectLesson(lesson.id)}
                          className={`w-full flex items-start gap-2.5 px-3 py-2 text-left text-xs transition-colors ${
                            isSelected
                              ? 'bg-sky-950/40 text-sky-200 border-l-2 border-sky-400 pl-[10px]'
                              : 'text-zinc-300 hover:bg-zinc-800/40'
                          }`}
                        >
                          <div className="mt-0.5 shrink-0">
                            {isCompleted ? (
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 fill-emerald-950" />
                            ) : (
                              <Circle className="w-3.5 h-3.5 text-zinc-600" />
                            )}
                          </div>

                          <div className="flex-1 min-w-0">
                            <div className="font-medium line-clamp-2 leading-tight">
                              {lesson.title}
                            </div>
                            <div className="flex items-center gap-2 mt-1.5 text-[10px] text-zinc-400">
                              {getDifficultyBadge(lesson.difficulty)}
                              <span className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {lesson.estimated_minutes} мин
                              </span>
                              {lesson.hints_count > 0 && (
                                <span className="flex items-center gap-1 text-amber-400/80">
                                  <HelpCircle className="w-3 h-3" />
                                  {lesson.hints_count}
                                </span>
                              )}
                            </div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
