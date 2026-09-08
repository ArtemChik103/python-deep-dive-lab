import { useEffect, useState } from 'react';
import confetti from 'canvas-confetti';
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
import type {
  EditorTab,
  EvaluationResponse,
  ExecutionResult,
  FileNode,
  HintItem,
  InstalledPackage,
  LessonDetail,
  ModuleItem,
  PopularPackage,
} from './types';

export function App() {
  // Navigation & Mode
  const [mode, setMode] = useState<'curriculum' | 'sandbox'>('curriculum');
  const [activeSidebarTab, setActiveSidebarTab] = useState<'curriculum' | 'files' | 'packages'>('curriculum');

  // Curriculum State
  const [modules, setModules] = useState<ModuleItem[]>([]);
  const [selectedLessonId, setSelectedLessonId] = useState<string | null>(null);
  const [currentLesson, setCurrentLesson] = useState<LessonDetail | null>(null);
  const [unlockedHints, setUnlockedHints] = useState<HintItem[]>([]);
  const [currentSolution, setCurrentSolution] = useState<string | null>(null);
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

  // Split Pane Resizing
  const theoryWidthPercent = 42;
  const consoleHeight = 240;

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

      // If no tabs open, open main.py if present
      if (tabs.length === 0) {
        const mainPy = res.files.find((f) => f.name === 'main.py');
        if (mainPy) {
          handleOpenFile(mainPy.path);
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
    const tab = tabs.find((t) => t.id === activeTabId);
    if (!tab) return;

    setIsRunning(true);
    setActiveConsoleTab('output');
    try {
      if (!tab.isLessonStarter && tab.isDirty) {
        await saveFile(tab.path, tab.content);
        setTabs((prev) => prev.map((t) => (t.id === tab.id ? { ...t, isDirty: false } : t)));
      }

      const res = tab.isLessonStarter
        ? await executeCode(tab.content)
        : await executeFile(tab.path);

      setExecResult(res);

      if (res.plots && res.plots.length > 0) {
        setActiveConsoleTab('plots');
      }
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
    try {
      const res = await evaluateLesson(selectedLessonId, codeToTest);
      setEvalResult(res);

      if (res.all_passed) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
        });
        setCompletedLessonIds((prev) => new Set([...prev, selectedLessonId]));
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
    } catch (err) {
      alert(`Ошибка получения решения: ${err}`);
    } finally {
      setIsLoadingSolution(false);
    }
  };

  // Apply solution to editor
  const handleApplySolutionToEditor = (solutionCode: string) => {
    if (!activeTabId) return;
    handleChangeContent(activeTabId, solutionCode);
  };

  // Pip actions
  const handleInstallPackage = async (packageName: string) => {
    setIsInstalling(true);
    setActiveConsoleTab('pip');
    setPipLogs(`[pip install ${packageName}] Выполняется установка пакета...\n`);
    try {
      const res = await installPackage(packageName);
      setPipLogs((prev) => prev + res.stdout + (res.stderr ? '\n' + res.stderr : ''));
      if (res.success) {
        setPipLogs((prev) => prev + `\n✓ Пакет ${packageName} успешно установлен!\n`);
        loadPackages();
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

  return (
    <div className="flex flex-col h-screen w-screen bg-zinc-950 text-zinc-100 overflow-hidden font-sans">
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
      />

      {/* Main Workspace Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Drawer Sidebar (Curriculum / Files / Pip) */}
        <aside className="w-72 md:w-80 shrink-0 h-full border-r border-zinc-800 bg-zinc-900">
          {activeSidebarTab === 'curriculum' && (
            <CurriculumTree
              modules={modules}
              selectedLessonId={selectedLessonId}
              onSelectLesson={(lessonId) => {
                loadLessonDetails(lessonId);
                if (mode !== 'curriculum') setMode('curriculum');
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
        </aside>

        {/* Center Canvas & Split Panes */}
        <main className="flex-1 flex flex-col h-full overflow-hidden bg-zinc-950">
          {/* Top Split Area: Theory (if in curriculum) + Editor */}
          <div className="flex-1 flex overflow-hidden">
            {/* Theory & Hints Pane (Only in Curriculum mode) */}
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
            />
          </div>
        </main>
      </div>
    </div>
  );
}
export default App;
