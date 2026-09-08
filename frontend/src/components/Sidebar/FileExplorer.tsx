import React, { useState } from 'react';
import {
  Folder,
  FolderOpen,
  FileCode2,
  FileText,
  FileJson,
  File,
  Plus,
  FolderPlus,
  RotateCcw,
  Trash2,
  Edit2,
  Check,
  X,
  ChevronRight,
  ChevronDown,
} from 'lucide-react';
import type { FileNode } from '../../types';

interface FileExplorerProps {
  files: FileNode[];
  activeFilePath: string | null;
  onOpenFile: (path: string) => void;
  onCreateFile: (path: string, isDirectory: boolean) => Promise<void>;
  onRenameFile: (oldPath: string, newPath: string) => Promise<void>;
  onDeleteFile: (path: string) => Promise<void>;
  onRefresh: () => void;
  onResetWorkspace: () => void;
}

export const FileExplorer: React.FC<FileExplorerProps> = ({
  files,
  activeFilePath,
  onOpenFile,
  onCreateFile,
  onRenameFile,
  onDeleteFile,
  onRefresh,
  onResetWorkspace,
}) => {
  const [openFolders, setOpenFolders] = useState<Record<string, boolean>>({});
  const [creatingType, setCreatingType] = useState<'file' | 'folder' | null>(null);
  const [newItemName, setNewItemName] = useState('');
  const [renamingPath, setRenamingPath] = useState<string | null>(null);
  const [renameValue, setRenameValue] = useState('');

  const toggleFolder = (path: string) => {
    setOpenFolders((prev) => ({
      ...prev,
      [path]: !prev[path],
    }));
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newItemName.trim()) return;
    try {
      await onCreateFile(newItemName.trim(), creatingType === 'folder');
      setNewItemName('');
      setCreatingType(null);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      alert(`Ошибка создания: ${msg}`);
    }
  };

  const handleRenameSubmit = async (oldPath: string) => {
    if (!renameValue.trim() || renameValue === oldPath) {
      setRenamingPath(null);
      return;
    }
    try {
      await onRenameFile(oldPath, renameValue.trim());
      setRenamingPath(null);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      alert(`Ошибка переименования: ${msg}`);
    }
  };

  const getFileIcon = (name: string, isDir: boolean, isOpen: boolean) => {
    if (isDir) {
      return isOpen ? (
        <FolderOpen className="w-4 h-4 text-amber-400 shrink-0" />
      ) : (
        <Folder className="w-4 h-4 text-amber-400 shrink-0" />
      );
    }
    if (name.endsWith('.py')) {
      return <FileCode2 className="w-4 h-4 text-sky-400 shrink-0" />;
    }
    if (name.endsWith('.json')) {
      return <FileJson className="w-4 h-4 text-emerald-400 shrink-0" />;
    }
    if (name.endsWith('.md') || name.endsWith('.txt')) {
      return <FileText className="w-4 h-4 text-zinc-400 shrink-0" />;
    }
    return <File className="w-4 h-4 text-zinc-400 shrink-0" />;
  };

  const renderTree = (nodes: FileNode[], depth = 0) => {
    return nodes.map((node) => {
      const isDir = node.is_directory;
      const isOpen = !!openFolders[node.path];
      const isActive = activeFilePath === node.path;
      const isRenaming = renamingPath === node.path;

      return (
        <div key={node.path} className="text-xs">
          <div
            className={`group flex items-center justify-between py-1 px-2 rounded-md hover:bg-zinc-800/60 cursor-pointer transition-colors ${
              isActive ? 'bg-zinc-800 text-sky-300 font-medium' : 'text-zinc-300'
            }`}
            style={{ paddingLeft: `${depth * 12 + 8}px` }}
            onClick={() => {
              if (isDir) {
                toggleFolder(node.path);
              } else {
                onOpenFile(node.path);
              }
            }}
          >
            <div className="flex items-center gap-1.5 min-w-0 flex-1">
              {isDir && (
                <span className="text-zinc-500">
                  {isOpen ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                </span>
              )}
              {getFileIcon(node.name, isDir, isOpen)}

              {isRenaming ? (
                <div
                  className="flex items-center gap-1 flex-1"
                  onClick={(e) => e.stopPropagation()}
                >
                  <input
                    type="text"
                    value={renameValue}
                    onChange={(e) => setRenameValue(e.target.value)}
                    autoFocus
                    className="w-full bg-zinc-950 border border-sky-500 px-1 py-0.5 rounded text-xs text-white"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleRenameSubmit(node.path);
                      if (e.key === 'Escape') setRenamingPath(null);
                    }}
                  />
                  <button
                    onClick={() => handleRenameSubmit(node.path)}
                    className="p-0.5 text-emerald-400 hover:bg-zinc-700 rounded"
                  >
                    <Check className="w-3 h-3" />
                  </button>
                  <button
                    onClick={() => setRenamingPath(null)}
                    className="p-0.5 text-rose-400 hover:bg-zinc-700 rounded"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ) : (
                <span className="truncate">{node.name}</span>
              )}
            </div>

            {!isRenaming && (
              <div
                className="opacity-0 group-hover:opacity-100 flex items-center gap-1 shrink-0"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  onClick={() => {
                    setRenamingPath(node.path);
                    setRenameValue(node.path);
                  }}
                  className="p-1 hover:text-sky-300 text-zinc-500 rounded transition-colors"
                  title="Переименовать"
                >
                  <Edit2 className="w-3 h-3" />
                </button>
                <button
                  onClick={() => {
                    if (confirm(`Удалить ${node.name}?`)) {
                      onDeleteFile(node.path);
                    }
                  }}
                  className="p-1 hover:text-rose-400 text-zinc-500 rounded transition-colors"
                  title="Удалить"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            )}
          </div>

          {isDir && isOpen && node.children && node.children.length > 0 && (
            <div>{renderTree(node.children, depth + 1)}</div>
          )}
        </div>
      );
    });
  };

  return (
    <div className="flex flex-col h-full bg-zinc-900 border-r border-zinc-800 select-none overflow-hidden">
      {/* Explorer Header */}
      <div className="p-3 border-b border-zinc-800 shrink-0 flex items-center justify-between">
        <span className="text-xs font-semibold text-zinc-300 uppercase tracking-wider">
          Файлы проекта
        </span>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setCreatingType('file')}
            className="p-1 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 rounded transition-colors"
            title="Новый .py файл"
          >
            <Plus className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setCreatingType('folder')}
            className="p-1 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 rounded transition-colors"
            title="Новая папка"
          >
            <FolderPlus className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={onRefresh}
            className="p-1 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 rounded transition-colors"
            title="Обновить список"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* New File / Folder Input Form */}
      {creatingType && (
        <form onSubmit={handleCreateSubmit} className="p-2 border-b border-zinc-800 bg-zinc-950/80">
          <div className="text-[11px] text-zinc-400 mb-1 flex items-center gap-1">
            {creatingType === 'file' ? <FileCode2 className="w-3 h-3 text-sky-400" /> : <Folder className="w-3 h-3 text-amber-400" />}
            <span>Создать {creatingType === 'file' ? 'файл' : 'папку'}:</span>
          </div>
          <div className="flex items-center gap-1">
            <input
              type="text"
              placeholder={creatingType === 'file' ? 'module.py' : 'utils'}
              value={newItemName}
              onChange={(e) => setNewItemName(e.target.value)}
              autoFocus
              className="flex-1 bg-zinc-900 border border-sky-500 rounded px-2 py-1 text-xs text-white placeholder-zinc-500 focus:outline-hidden"
            />
            <button
              type="submit"
              className="px-2 py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs"
            >
              OK
            </button>
            <button
              type="button"
              onClick={() => setCreatingType(null)}
              className="p-1 text-zinc-400 hover:text-zinc-200"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </form>
      )}

      {/* File Tree List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
        {files.length === 0 ? (
          <div className="p-4 text-center text-xs text-zinc-500">
            В рабочей директории нет файлов
          </div>
        ) : (
          renderTree(files)
        )}
      </div>

      {/* Footer / Reset Workspace */}
      <div className="p-2.5 border-t border-zinc-800 bg-zinc-950/40">
        <button
          onClick={() => {
            if (confirm('Сбросить рабочую директорию к начальным шаблонам (main.py, math_utils.py)?')) {
              onResetWorkspace();
            }
          }}
          className="w-full flex items-center justify-center gap-1.5 py-1.5 px-2 bg-zinc-800/80 hover:bg-zinc-800 text-zinc-300 text-xs rounded transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5 text-zinc-400" />
          <span>Сбросить шаблоны</span>
        </button>
      </div>
    </div>
  );
};
