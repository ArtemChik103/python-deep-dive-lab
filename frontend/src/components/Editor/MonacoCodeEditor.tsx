import React from 'react';
import Editor from '@monaco-editor/react';
import { X, FileCode2, Save } from 'lucide-react';
import type { EditorTab } from '../../types';

interface MonacoCodeEditorProps {
  tabs: EditorTab[];
  activeTabId: string | null;
  onSelectTab: (tabId: string) => void;
  onCloseTab: (tabId: string) => void;
  onChangeContent: (tabId: string, newContent: string) => void;
  onSave: () => void;
  onRun: () => void;
}

export const MonacoCodeEditor: React.FC<MonacoCodeEditorProps> = ({
  tabs,
  activeTabId,
  onSelectTab,
  onCloseTab,
  onChangeContent,
  onSave,
  onRun,
}) => {
  const activeTab = tabs.find((t) => t.id === activeTabId);

  const handleEditorMount = (editor: any, monaco: any) => {
    // Add Ctrl+Enter shortcut to run code
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      onRun();
    });

    // Add Ctrl+S shortcut to save file
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      onSave();
    });
  };

  return (
    <div className="flex flex-col h-full bg-[#1e1e1e] overflow-hidden select-none">
      {/* Tabs Header Bar */}
      <div className="h-9 bg-zinc-950 border-b border-zinc-800 flex items-center justify-between px-2 shrink-0">
        <div className="flex items-center gap-1 overflow-x-auto h-full max-w-full">
          {tabs.map((tab) => {
            const isActive = tab.id === activeTabId;

            return (
              <div
                key={tab.id}
                onClick={() => onSelectTab(tab.id)}
                className={`group flex items-center gap-2 h-full px-3 text-xs border-r border-zinc-800 cursor-pointer transition-colors ${
                  isActive
                    ? 'bg-[#1e1e1e] text-sky-400 border-t-2 border-t-sky-500 font-medium'
                    : 'bg-zinc-950 text-zinc-400 hover:bg-zinc-900 hover:text-zinc-300'
                }`}
              >
                <FileCode2 className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate max-w-[140px]">{tab.name}</span>

                {/* Dirty Indicator or Close Button */}
                <div className="flex items-center ml-1">
                  {tab.isDirty && (
                    <span className="w-2 h-2 rounded-full bg-amber-400 mr-1" title="Не сохранено" />
                  )}
                  {tabs.length > 1 && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onCloseTab(tab.id);
                      }}
                      className="opacity-0 group-hover:opacity-100 hover:bg-zinc-700/60 p-0.5 rounded text-zinc-400 hover:text-white transition-opacity"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Save indicator button */}
        {activeTab && (
          <div className="flex items-center gap-2 pr-2">
            <button
              onClick={onSave}
              className={`flex items-center gap-1 text-[11px] px-2 py-0.5 rounded transition-colors ${
                activeTab.isDirty
                  ? 'bg-amber-950 text-amber-300 border border-amber-800 hover:bg-amber-900'
                  : 'text-zinc-500 hover:text-zinc-300'
              }`}
              title="Сохранить файл (Ctrl+S)"
            >
              <Save className="w-3 h-3" />
              <span>{activeTab.isDirty ? 'Сохранить' : 'Сохранено'}</span>
            </button>
          </div>
        )}
      </div>

      {/* Editor Main Canvas */}
      <div className="flex-1 w-full h-full relative">
        {activeTab ? (
          <Editor
            height="100%"
            language="python"
            theme="vs-dark"
            value={activeTab.content}
            onChange={(val) => onChangeContent(activeTab.id, val || '')}
            onMount={handleEditorMount}
            options={{
              fontSize: 13,
              fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
              fontLigatures: true,
              minimap: { enabled: true, scale: 0.75 },
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: 4,
              insertSpaces: true,
              wordWrap: 'on',
              lineNumbers: 'on',
              folding: true,
              renderWhitespace: 'selection',
              renderLineHighlight: 'all',
              fixedOverflowWidgets: true,
            }}
          />
        ) : (
          <div className="flex items-center justify-center h-full text-zinc-500 text-xs">
            Нет открытых файлов для редактирования
          </div>
        )}
      </div>
    </div>
  );
};
