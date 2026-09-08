import { useEffect, useState } from 'react';
import confetti from 'canvas-confetti';
import { X, BookOpen, FolderTree, Package } from 'lucide-react';
import {
  createFileOrFolder,
  deleteFile,
  evaluateLesson,
  executeCode,
  executeFile,
  fetchFileTree,
  fetchHint,
  fetchInstalledPackages,
  fetchLesson,
  fetchModules,
  fetchPopularPackages,
  fetchSolution,
  installPackage,
  readFile,
  renameFile,
  resetWorkspace,
  saveFile,
  uninstallPackage,
} from './api/client';
import { MonacoCodeEditor } from './components/Editor/MonacoCodeEditor';
import { TopNavbar } from './components/Layout/TopNavbar';
import { TheoryPane } from './components/Lesson/TheoryPane';
import { ConsolePanel } from './components/Output/ConsolePanel';
import { CurriculumTree } from './components/Sidebar/CurriculumTree';
import { FileExplorer } from './components/Sidebar/FileExplorer';
import { PackageManager } from './components/Sidebar/PackageManager';
import { ProfileModal } from './components/Profile/ProfileModal';
import {
  getUserProfile,
  saveUserProfile,
  getLessonStatsMap,
  getAchievements,
  incrementRunCount,
  recordTestAttempt,
  evaluateAllAchievements,
  computeOverview,
} from './services/progressService';
import type {
  Achievement,
  EditorTab,
  EvaluationResponse,
  ExecutionResult,
  FileNode,
  HintItem,
  InstalledPackage,
  LessonDetail,
  LessonSolutionStats,
  ModuleItem,
  PopularPackage,
  UserProfile,
} from './types';

export function App() {
  // Mobile Responsiveness State
  const [isMobile, setIsMobile] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return window.innerWidth < 768;
    }
    return false;
  });
  const [mobileActiveView, setMobileActiveView] = useState<'theory' | 'editor' | 'console'>('theory');
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  // Navigation & Mode
  const [mode, setMode] = useState<'curriculum' | 'sandbox'>('curriculum');
  const [activeSidebarTab, setActiveSidebarTab] = useState<'curriculum' | 'files' | 'packages'>('curriculum');

  // Curriculum State
  const [modules, setModules] = useState<ModuleItem[]>([]);
  const [selectedLessonId, setSelectedLessonId] = useState<string | null>(null);
  const [currentLesson, setCurrentLesson] = useState<LessonDetail | null>(null);
  const [unlockedHints, setUnlockedHints] = useState<HintItem[]>([]);
  const [currentSolution, setCurrentSolution] = useState<string | null>(null);
  const [revealedSolutionLessons, setRevealedSolutionLessons] = useState<Set<string>>(new Set());
  const [copiedSolutionLessons, setCopiedSolutionLessons] = useState<Set<string>>(new Set());
  const [completedLessonIds, setCompletedLessonIds] = useState<Set<string>>(() => {
    try {
      const saved = localStorage.getItem('pydeep_completed_lessons');
      return saved ? new Set(JSON.parse(saved)) : new Set();
    } catch {
      return new Set();
    }
  });

  // Files & Editor State
  const [files, setFiles] = useState<FileNode[]>([]);
  const [tabs, setTabs] = useState<EditorTab[]>([]);
  const [activeTabId, setActiveTabId] = useState<string | null>(null);

  // Packages State
  const [installedPackages, setInstalledPackages] = useState<InstalledPackage[]>([]);
  const [popularPackages, setPopularPackages] = useState<PopularPackage[]>([]);
  const [isInstalling, setIsInstalling] = useState(false);
  const [pipLogs, setPipLogs] = useState<string>('');

  // Execution & Output State
  const [isRunning, setIsRunning] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [isLoadingHint, setIsLoadingHint] = useState(false);
  const [isLoadingSolution, setIsLoadingSolution] = useState(false);
  const [activeConsoleTab, setActiveConsoleTab] = useState<'output' | 'tests' | 'plots' | 'pip'>('output');
  const [execResult, setExecResult] = useState<ExecutionResult | null>(null);
  const [evalResult, setEvalResult] = useState<EvaluationResponse | null>(null);

  // User Profile, Solution Accuracy & Achievements State
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile>(getUserProfile);
  const [lessonStatsMap, setLessonStatsMap] = useState<Record<string, LessonSolutionStats>>(getLessonStatsMap);
  const [achievements, setAchievements] = useState<Achievement[]>(getAchievements);

  // Derived Progress & Accuracy Overview
  const progressOverview = computeOverview(modules, lessonStatsMap, achievements);

  // Split Pane Resizing for Desktop
  const theoryWidthPercent = 42;
  const consoleHeight = 240;

  // Window resize listener
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Initial Data Fetch
  useEffect(() => {
    loadCurriculum();
    loadWorkspaceFiles();
    loadPackages();
  }, []);

  // Sync completed lessons to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('pydeep_completed_lessons', JSON.stringify([...completedLessonIds]));
    } catch {
      // ignore
    }
  }, [completedLessonIds]);

  const loadCurriculum = async () => {
    try {
      const data = await fetchModules();
      setModules(data.modules);
      if (data.modules.length > 0 && data.modules[0].lessons.length > 0) {
        const firstLessonId = data.modules[0].lessons[0].id;
        loadLessonDetails(firstLessonId);
      }
    } catch (err) {
      console.error('Error loading curriculum:', err);
    }
  };

  const loadLessonDetails = async (lessonId: string) => {
    try {
      setSelectedLessonId(lessonId);
      const lesson = await fetchLesson(lessonId);
      setCurrentLesson(lesson);
      setUnlockedHints([]);
      setCurrentSolution(null);

      // Open starter code tab in editor
      const tabId = `lesson_${lesson.id}`;
      const existingTab = tabs.find((t) => t.id === tabId);
      if (!existingTab) {
        const newTab: EditorTab = {
          id: tabId,
          name: `${lesson.id}.py`,
          path: `${lesson.id}.py`,
          content: lesson.starter_code,
          isDirty: false,
          isLessonStarter: true,
        };
        setTabs((prev) => [newTab, ...prev.filter((t) => !t.isLessonStarter)]);
        setActiveTabId(tabId);
      } else {
        setActiveTabId(tabId);
      }
    } catch (err) {
      console.error('Error fetching lesson:', err);
    }
  };

  const loadWorkspaceFiles = async () => {
    try {
      const res = await fetchFileTree();
      setFiles(res.files);

      if (tabs.length === 0) {
        const mainPy = res.files.find((f) => f.name === 'main.py');
        if (mainPy) {
          try {
            const fileData = await readFile(mainPy.path);
            const newTab: EditorTab = {
              id: `file_${mainPy.path}`,
              name: 'main.py',
              path: mainPy.path,
              content: fileData.content,
              isDirty: false,
            };
            setTabs((prev) => (prev.some((t) => t.id === newTab.id) ? prev : [...prev, newTab]));
          } catch {
            // ignore initial preload error
          }
        }
      }
    } catch (err) {
      console.error('Error loading workspace files:', err);
    }
  };

  const loadPackages = async () => {
    try {
      const [inst, pop] = await Promise.all([fetchInstalledPackages(), fetchPopularPackages()]);
      setInstalledPackages(inst.packages);
      setPopularPackages(pop.packages);
    } catch (err) {
      console.error('Error loading packages:', err);
    }
  };

  // Open file in editor tab
  const handleOpenFile = async (path: string) => {
    const existing = tabs.find((t) => t.path === path);
    if (existing) {
      setActiveTabId(existing.id);
      if (isMobile) {
        setMobileActiveView('editor');
        setIsMobileSidebarOpen(false);
      }
      return;
    }
    try {
      const fileData = await readFile(path);
      const fileName = path.split('/').pop() || path;
      const newTab: EditorTab = {
        id: `file_${path}`,
        name: fileName,
        path: path,
        content: fileData.content,
        isDirty: false,
      };
      setTabs((prev) => [...prev, newTab]);
      setActiveTabId(newTab.id);
      if (isMobile) {
        setMobileActiveView('editor');
        setIsMobileSidebarOpen(false);
      }
    } catch (err) {
      alert(`Ошибка чтения файла: ${err}`);
    }
  };

  // Close tab
  const handleCloseTab = (tabId: string) => {
    const remaining = tabs.filter((t) => t.id !== tabId);
    setTabs(remaining);
    if (activeTabId === tabId) {
      setActiveTabId(remaining.length > 0 ? remaining[remaining.length - 1].id : null);
    }
  };

  // Edit tab content
  const handleChangeContent = (tabId: string, newContent: string) => {
    setTabs((prev) =>
      prev.map((t) => (t.id === tabId ? { ...t, content: newContent, isDirty: true } : t))
    );
  };

  // Save current active file
  const handleSaveFile = async () => {
    const tab = tabs.find((t) => t.id === activeTabId);
    if (!tab) return;
    try {
      await saveFile(tab.path, tab.content);
      setTabs((prev) => prev.map((t) => (t.id === tab.id ? { ...t, isDirty: false } : t)));
      loadWorkspaceFiles();
    } catch (err) {
      alert(`Ошибка сохранения файла: ${err}`);
    }
  };

  // Run Code (Ctrl+Enter)
  const handleRunCode = async () => {
    let tab = tabs.find((t) => t.id === activeTabId);
    if (!tab && tabs.length > 0) {
      tab = tabs[0];
    }
    const codeToRun = tab ? tab.content : (currentLesson?.starter_code || '');
    if (!codeToRun && !tab) return;

    setIsRunning(true);
    setActiveConsoleTab('output');
    if (isMobile) setMobileActiveView('console');

    try {
      if (tab && !tab.isLessonStarter && tab.isDirty) {
        await saveFile(tab.path, tab.content);
        setTabs((prev) => prev.map((t) => (t.id === tab!.id ? { ...t, isDirty: false } : t)));
      }

      incrementRunCount();
      const res = (!tab || tab.isLessonStarter)
        ? await executeCode(codeToRun)
        : await executeFile(tab.path);

      setExecResult(res);

      if (res.plots && res.plots.length > 0) {
        setActiveConsoleTab('plots');
      }

      const { updatedAchievements } = evaluateAllAchievements(lessonStatsMap, {
        hasPlot: Boolean(res.plots && res.plots.length > 0),
      });
      setAchievements(updatedAchievements);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setExecResult({
        stdout: '',
        stderr: `Ошибка выполнения: ${msg}`,
        returncode: -1,
        timed_out: false,
        execution_time_ms: 0,
        plots: [],
      });
    } finally {
      setIsRunning(false);
    }
  };

  // Run Tests (Grader)
  const handleRunTests = async () => {
    if (!selectedLessonId) return;
    const tab = tabs.find((t) => t.id === activeTabId);
    const codeToTest = tab ? tab.content : currentLesson?.starter_code || '';

    setIsTesting(true);
    setActiveConsoleTab('tests');
    if (isMobile) setMobileActiveView('console');

    try {
      const res = await evaluateLesson(selectedLessonId, codeToTest);
      setEvalResult(res);

      if (currentLesson) {
        const isSolutionRevealed = Boolean(
          currentSolution ||
          revealedSolutionLessons.has(selectedLessonId) ||
          copiedSolutionLessons.has(selectedLessonId) ||
          lessonStatsMap[selectedLessonId]?.solutionRevealed
        );
        const isSolutionCopied = Boolean(
          copiedSolutionLessons.has(selectedLessonId) ||
          lessonStatsMap[selectedLessonId]?.solutionCopied
        );

        const { updatedStats, updatedAchievements } = recordTestAttempt({
          lessonId: currentLesson.id,
          lessonTitle: currentLesson.title,
          moduleTitle: currentLesson.module_title,
          difficulty: currentLesson.difficulty,
          passedCount: res.passed_tests,
          totalTests: res.total_tests,
          allPassed: res.all_passed,
          executionTimeMs: res.execution_time_ms,
          hintsUsed: unlockedHints.length,
          solutionRevealed: isSolutionRevealed,
          solutionCopied: isSolutionCopied,
        });
        setLessonStatsMap(updatedStats);
        setAchievements(updatedAchievements);

        if (res.all_passed) {
          if (!isSolutionRevealed) {
            confetti({
              particleCount: 80,
              spread: 70,
              origin: { y: 0.6 },
            });
          }
          setCompletedLessonIds((prev) => new Set([...prev, selectedLessonId]));
        }
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setEvalResult({
        all_passed: false,
        total_tests: 0,
        passed_tests: 0,
        test_cases: [],
        stdout: '',
        stderr: `Ошибка запуска автотестов: ${msg}`,
        execution_time_ms: 0,
        timed_out: false,
      });
    } finally {
      setIsTesting(false);
    }
  };

  // Reset code to starter code
  const handleResetCode = () => {
    if (mode === 'curriculum' && currentLesson) {
      if (confirm('Сбросить редактор к исходному коду задания?')) {
        const tabId = `lesson_${currentLesson.id}`;
        setTabs((prev) =>
          prev.map((t) => (t.id === tabId ? { ...t, content: currentLesson.starter_code, isDirty: false } : t))
        );
      }
    } else {
      loadWorkspaceFiles();
    }
  };

  // Unlock next hint
  const handleUnlockNextHint = async () => {
    if (!selectedLessonId || !currentLesson) return;
    const nextLevel = unlockedHints.length + 1;
    if (nextLevel > currentLesson.total_hints) return;

    setIsLoadingHint(true);
    try {
      const hint = await fetchHint(selectedLessonId, nextLevel);
      setUnlockedHints((prev) => [...prev, hint]);
    } catch (err) {
      alert(`Ошибка получения подсказки: ${err}`);
    } finally {
      setIsLoadingHint(false);
    }
  };

  // Reveal canonical solution
  const handleRevealSolution = async () => {
    if (!selectedLessonId) return;
    setIsLoadingSolution(true);
    try {
      const sol = await fetchSolution(selectedLessonId);
      setCurrentSolution(sol.solution);
      setRevealedSolutionLessons((prev) => new Set([...prev, selectedLessonId]));
    } catch (err) {
      alert(`Ошибка получения решения: ${err}`);
    } finally {
      setIsLoadingSolution(false);
    }
  };

  // Apply solution to editor
  const handleApplySolutionToEditor = (solutionCode: string) => {
    if (!activeTabId || !selectedLessonId) return;
    setRevealedSolutionLessons((prev) => new Set([...prev, selectedLessonId]));
    setCopiedSolutionLessons((prev) => new Set([...prev, selectedLessonId]));
    handleChangeContent(activeTabId, solutionCode);
    if (isMobile) setMobileActiveView('editor');
  };

  // Pip actions
  const handleInstallPackage = async (packageName: string) => {
    setIsInstalling(true);
    setActiveConsoleTab('pip');
    if (isMobile) setMobileActiveView('console');
    setPipLogs(`[pip install ${packageName}] Выполняется установка пакета...\n`);
    try {
      const res = await installPackage(packageName);
      setPipLogs((prev) => prev + res.stdout + (res.stderr ? '\n' + res.stderr : ''));
      if (res.success) {
        setPipLogs((prev) => prev + `\n✓ Пакет ${packageName} успешно установлен!\n`);
        loadPackages();
        const { updatedAchievements } = evaluateAllAchievements(lessonStatsMap, { hasPackage: true });
        setAchievements(updatedAchievements);
      } else {
        setPipLogs((prev) => prev + `\n✗ Ошибка установки ${packageName}.\n`);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setPipLogs((prev) => prev + `\nОшибка: ${msg}\n`);
    } finally {
      setIsInstalling(false);
    }
  };

  const handleUninstallPackage = async (packageName: string) => {
    setIsInstalling(true);
    setActiveConsoleTab('pip');
    if (isMobile) setMobileActiveView('console');
    setPipLogs(`[pip uninstall ${packageName}] Удаление пакета...\n`);
    try {
      const res = await uninstallPackage(packageName);
      setPipLogs((prev) => prev + res.stdout + (res.stderr ? '\n' + res.stderr : ''));
      if (res.success) {
        setPipLogs((prev) => prev + `\n✓ Пакет ${packageName} успешно удален.\n`);
        loadPackages();
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      setPipLogs((prev) => prev + `\nОшибка: ${msg}\n`);
    } finally {
      setIsInstalling(false);
    }
  };

  const totalLessonsCount = modules.reduce((acc, m) => acc + m.total_lessons, 0);

  // Sidebar component content
  const renderSidebarContent = () => (
    <>
      {activeSidebarTab === 'curriculum' && (
        <CurriculumTree
          modules={modules}
          selectedLessonId={selectedLessonId}
          onSelectLesson={(lessonId) => {
            loadLessonDetails(lessonId);
            if (mode !== 'curriculum') setMode('curriculum');
            if (isMobile) {
              setMobileActiveView('theory');
              setIsMobileSidebarOpen(false);
            }
          }}
          completedLessonIds={completedLessonIds}
        />
      )}

      {activeSidebarTab === 'files' && (
        <FileExplorer
          files={files}
          activeFilePath={tabs.find((t) => t.id === activeTabId)?.path || null}
          onOpenFile={handleOpenFile}
          onCreateFile={async (path, isDir) => {
            await createFileOrFolder(path, isDir);
            await loadWorkspaceFiles();
            if (!isDir) handleOpenFile(path);
          }}
          onRenameFile={async (oldPath, newPath) => {
            await renameFile(oldPath, newPath);
            await loadWorkspaceFiles();
          }}
          onDeleteFile={async (path) => {
            await deleteFile(path);
            await loadWorkspaceFiles();
            const openedTab = tabs.find((t) => t.path === path);
            if (openedTab) handleCloseTab(openedTab.id);
          }}
          onRefresh={loadWorkspaceFiles}
          onResetWorkspace={async () => {
            await resetWorkspace();
            await loadWorkspaceFiles();
          }}
        />
      )}

      {activeSidebarTab === 'packages' && (
        <PackageManager
          installed={installedPackages}
          popular={popularPackages}
          onInstall={handleInstallPackage}
          onUninstall={handleUninstallPackage}
          onRefresh={loadPackages}
          isInstalling={isInstalling}
        />
      )}
    </>
  );

  return (
    <div className="flex flex-col h-[100dvh] w-screen bg-zinc-950 text-zinc-100 overflow-hidden font-sans">
      {/* Top Navbar */}
      <TopNavbar
        mode={mode}
        setMode={setMode}
        activeSidebarTab={activeSidebarTab}
        setActiveSidebarTab={setActiveSidebarTab}
        onRunCode={handleRunCode}
        onRunTests={handleRunTests}
        onResetCode={handleResetCode}
        isRunning={isRunning}
        isTesting={isTesting}
        completedCount={completedLessonIds.size}
        totalLessons={totalLessonsCount}
        installedPackagesCount={installedPackages.length}
        userLevel={progressOverview.level}
        userAccuracy={progressOverview.overallAccuracy}
        onOpenProfile={() => setIsProfileModalOpen(true)}
        isMobile={isMobile}
        mobileActiveView={mobileActiveView}
        setMobileActiveView={setMobileActiveView}
        onToggleMobileSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
      />

      {/* Mobile Drawer (Off-canvas sidebar overlay) */}
      {isMobile && isMobileSidebarOpen && (
        <div className="fixed inset-0 z-50 flex">
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-xs transition-opacity"
            onClick={() => setIsMobileSidebarOpen(false)}
          />

          {/* Drawer Content */}
          <div className="relative w-4/5 max-w-sm h-full bg-zinc-900 border-r border-zinc-800 shadow-2xl flex flex-col z-10 animate-in slide-in-from-left duration-200">
            {/* Drawer User Profile Banner */}
            <div className="p-3 bg-gradient-to-r from-zinc-950 to-sky-950/40 border-b border-zinc-800 flex items-center justify-between">
              <div className="flex items-center gap-2.5 min-w-0">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center font-bold text-xs text-white shrink-0 shadow-xs">
                  {progressOverview.level}
                </div>
                <div className="min-w-0">
                  <div className="text-xs font-semibold text-white truncate">{userProfile.name}</div>
                  <div className="text-[10px] text-emerald-400 font-mono">
                    {progressOverview.overallAccuracy}% точность • {progressOverview.unlockedAchievementsCount} ачивок
                  </div>
                </div>
              </div>
              <button
                onClick={() => {
                  setIsMobileSidebarOpen(false);
                  setIsProfileModalOpen(true);
                }}
                className="px-2 py-1 text-[11px] bg-sky-950 hover:bg-sky-900 border border-sky-800 text-sky-300 rounded font-medium cursor-pointer shrink-0"
              >
                Профиль →
              </button>
            </div>

            {/* Drawer Header with tab selector */}
            <div className="p-3 border-b border-zinc-800 flex items-center justify-between bg-zinc-950">
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setActiveSidebarTab('curriculum')}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors ${
                    activeSidebarTab === 'curriculum' ? 'bg-zinc-800 text-sky-400' : 'text-zinc-400'
                  }`}
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Курс</span>
                </button>
                <button
                  onClick={() => setActiveSidebarTab('files')}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors ${
                    activeSidebarTab === 'files' ? 'bg-zinc-800 text-amber-400' : 'text-zinc-400'
                  }`}
                >
                  <FolderTree className="w-3.5 h-3.5" />
                  <span>Файлы</span>
                </button>
                <button
                  onClick={() => setActiveSidebarTab('packages')}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors ${
                    activeSidebarTab === 'packages' ? 'bg-zinc-800 text-emerald-400' : 'text-zinc-400'
                  }`}
                >
                  <Package className="w-3.5 h-3.5" />
                  <span>Pip</span>
                </button>
              </div>

              <button
                onClick={() => setIsMobileSidebarOpen(false)}
                className="p-1.5 text-zinc-400 hover:text-white rounded-md hover:bg-zinc-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Drawer Body */}
            <div className="flex-1 overflow-hidden">
              {renderSidebarContent()}
            </div>
          </div>
        </div>
      )}

      {/* Main Workspace Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Desktop Left Sidebar */}
        {!isMobile && (
          <aside className="w-72 md:w-80 shrink-0 h-full border-r border-zinc-800 bg-zinc-900 overflow-hidden">
            {renderSidebarContent()}
          </aside>
        )}

        {/* Center Canvas */}
        <main className="flex-1 flex flex-col h-full overflow-hidden bg-zinc-950">
          {/* MOBILE VIEW HANDLING */}
          {isMobile ? (
            <div className="flex-1 w-full h-full overflow-hidden relative">
              {/* Mobile View 1: Theory */}
              {mobileActiveView === 'theory' && mode === 'curriculum' && currentLesson && (
                <div className="w-full h-full overflow-y-auto">
                  <TheoryPane
                    lesson={currentLesson}
                    unlockedHints={unlockedHints}
                    onUnlockNextHint={handleUnlockNextHint}
                    onRevealSolution={handleRevealSolution}
                    solution={currentSolution}
                    onApplySolutionToEditor={handleApplySolutionToEditor}
                    isLoadingHint={isLoadingHint}
                    isLoadingSolution={isLoadingSolution}
                    onGoToEditor={() => setMobileActiveView('editor')}
                  />
                </div>
              )}

              {/* Mobile View 2: Code Editor */}
              {mobileActiveView === 'editor' && (
                <div className="w-full h-full overflow-hidden">
                  <MonacoCodeEditor
                    tabs={tabs}
                    activeTabId={activeTabId}
                    onSelectTab={setActiveTabId}
                    onCloseTab={handleCloseTab}
                    onChangeContent={handleChangeContent}
                    onSave={handleSaveFile}
                    onRun={handleRunCode}
                  />
                </div>
              )}

              {/* Mobile View 3: Console / Tests */}
              {mobileActiveView === 'console' && (
                <div className="w-full h-full overflow-hidden">
                  <ConsolePanel
                    activeTab={activeConsoleTab}
                    setActiveTab={setActiveConsoleTab}
                    execResult={execResult}
                    evalResult={evalResult}
                    pipLogs={pipLogs}
                    onClearOutput={() => {
                      setExecResult(null);
                      setEvalResult(null);
                      setPipLogs('');
                    }}
                    isSolutionRevealed={Boolean(
                      currentSolution ||
                      (selectedLessonId && revealedSolutionLessons.has(selectedLessonId)) ||
                      (selectedLessonId && lessonStatsMap[selectedLessonId]?.solutionRevealed)
                    )}
                  />
                </div>
              )}
            </div>
          ) : (
            /* DESKTOP SPLIT VIEW */
            <>
              <div className="flex-1 flex overflow-hidden">
                {/* Theory & Hints Pane (Curriculum mode) */}
                {mode === 'curriculum' && currentLesson && (
                  <div
                    className="h-full border-r border-zinc-800 shrink-0 overflow-hidden"
                    style={{ width: `${theoryWidthPercent}%` }}
                  >
                    <TheoryPane
                      lesson={currentLesson}
                      unlockedHints={unlockedHints}
                      onUnlockNextHint={handleUnlockNextHint}
                      onRevealSolution={handleRevealSolution}
                      solution={currentSolution}
                      onApplySolutionToEditor={handleApplySolutionToEditor}
                      isLoadingHint={isLoadingHint}
                      isLoadingSolution={isLoadingSolution}
                    />
                  </div>
                )}

                {/* Monaco Editor Canvas */}
                <div className="flex-1 h-full overflow-hidden">
                  <MonacoCodeEditor
                    tabs={tabs}
                    activeTabId={activeTabId}
                    onSelectTab={setActiveTabId}
                    onCloseTab={handleCloseTab}
                    onChangeContent={handleChangeContent}
                    onSave={handleSaveFile}
                    onRun={handleRunCode}
                  />
                </div>
              </div>

              {/* Bottom Console Panel */}
              <div
                className="shrink-0 transition-all border-t border-zinc-800"
                style={{ height: `${consoleHeight}px` }}
              >
                <ConsolePanel
                  activeTab={activeConsoleTab}
                  setActiveTab={setActiveConsoleTab}
                  execResult={execResult}
                  evalResult={evalResult}
                  pipLogs={pipLogs}
                  onClearOutput={() => {
                    setExecResult(null);
                    setEvalResult(null);
                    setPipLogs('');
                  }}
                  isSolutionRevealed={Boolean(
                    currentSolution ||
                    (selectedLessonId && revealedSolutionLessons.has(selectedLessonId)) ||
                    (selectedLessonId && lessonStatsMap[selectedLessonId]?.solutionRevealed)
                  )}
                />
              </div>
            </>
          )}
        </main>
      </div>

      {/* User Profile & Achievements Modal */}
      <ProfileModal
        isOpen={isProfileModalOpen}
        onClose={() => setIsProfileModalOpen(false)}
        profile={userProfile}
        onUpdateProfile={(updated) => {
          setUserProfile(updated);
          saveUserProfile(updated);
        }}
        overview={progressOverview}
        statsMap={lessonStatsMap}
        achievements={achievements}
        modules={modules}
        onSelectLesson={(lessonId) => {
          loadLessonDetails(lessonId);
          setIsProfileModalOpen(false);
        }}
        onResetProgress={() => {
          localStorage.removeItem('pydeep_lesson_stats_v2');
          localStorage.removeItem('pydeep_achievements_v2');
          localStorage.removeItem('pydeep_completed_lessons');
          localStorage.removeItem('pydeep_run_count');
          setLessonStatsMap({});
          setAchievements(getAchievements());
          setCompletedLessonIds(new Set());
        }}
      />
    </div>
  );
}
export default App;
