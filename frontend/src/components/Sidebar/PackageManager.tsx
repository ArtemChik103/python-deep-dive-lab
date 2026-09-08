import React, { useState } from 'react';
import {
  Package,
  Plus,
  Download,
  Trash2,
  ExternalLink,
  Search,
  RotateCcw,
  Sparkles,
} from 'lucide-react';
import type { InstalledPackage, PopularPackage } from '../../types';

interface PackageManagerProps {
  installed: InstalledPackage[];
  popular: PopularPackage[];
  onInstall: (packageName: string) => Promise<void>;
  onUninstall: (packageName: string) => Promise<void>;
  onRefresh: () => void;
  isInstalling: boolean;
}

export const PackageManager: React.FC<PackageManagerProps> = ({
  installed,
  popular,
  onInstall,
  onUninstall,
  onRefresh,
  isInstalling,
}) => {
  const [installInput, setInstallInput] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const handleInstallSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!installInput.trim()) return;
    const pkg = installInput.trim();
    setInstallInput('');
    await onInstall(pkg);
  };

  const installedNames = new Set(installed.map((p) => p.name.toLowerCase()));

  const filteredInstalled = installed.filter((p) =>
    p.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col h-full bg-zinc-900 border-r border-zinc-800 select-none overflow-hidden">
      {/* Header */}
      <div className="p-3 border-b border-zinc-800 shrink-0 space-y-2.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            <Package className="w-4 h-4 text-emerald-400" />
            <span className="text-xs font-semibold text-zinc-200 uppercase tracking-wider">
              Менеджер пакетов Pip
            </span>
          </div>
          <button
            onClick={onRefresh}
            className="p-1 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 rounded transition-colors"
            title="Обновить список установленных"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Install Input Form */}
        <form onSubmit={handleInstallSubmit} className="flex items-center gap-1.5">
          <input
            type="text"
            placeholder="pip install <пакет>..."
            value={installInput}
            onChange={(e) => setInstallInput(e.target.value)}
            disabled={isInstalling}
            className="flex-1 px-2.5 py-1.5 bg-zinc-950 border border-zinc-800 rounded-md text-xs text-white placeholder-zinc-500 focus:outline-hidden focus:border-emerald-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isInstalling || !installInput.trim()}
            className="flex items-center gap-1 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded-md text-xs font-medium transition-colors"
          >
            {isInstalling ? (
              <span className="animate-spin text-xs">⏳</span>
            ) : (
              <Plus className="w-3.5 h-3.5" />
            )}
            <span>Установить</span>
          </button>
        </form>

        {/* Search */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Фильтр библиотек..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1 bg-zinc-950/60 border border-zinc-800/80 rounded text-xs text-zinc-300 placeholder-zinc-600 focus:outline-hidden focus:border-zinc-700"
          />
        </div>
      </div>

      {/* Installed Packages List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-4">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
              Установлено в venv ({filteredInstalled.length})
            </span>
          </div>

          <div className="space-y-1">
            {filteredInstalled.length === 0 ? (
              <div className="text-xs text-zinc-500 py-2 italic text-center">
                Нет установленных библиотек
              </div>
            ) : (
              filteredInstalled.map((pkg) => (
                <div
                  key={pkg.name}
                  className="flex items-center justify-between px-2.5 py-1.5 rounded-md bg-zinc-950/70 border border-zinc-800/60 hover:border-zinc-700 text-xs transition-colors"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="font-mono text-zinc-200 truncate">{pkg.name}</span>
                    <span className="text-[10px] font-mono text-zinc-500 bg-zinc-900 px-1.5 py-0.5 rounded border border-zinc-800">
                      v{pkg.version}
                    </span>
                  </div>

                  <button
                    onClick={() => {
                      if (confirm(`Удалить пакет ${pkg.name}?`)) {
                        onUninstall(pkg.name);
                      }
                    }}
                    className="p-1 text-zinc-500 hover:text-rose-400 rounded transition-colors"
                    title="Удалить пакет"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recommended Libraries Section */}
        <div>
          <div className="flex items-center gap-1.5 mb-2">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
              Популярные для изучения
            </span>
          </div>

          <div className="space-y-1.5">
            {popular.map((item) => {
              const isAdded = installedNames.has(item.name.toLowerCase());

              return (
                <div
                  key={item.name}
                  className="p-2.5 rounded-md bg-zinc-950/40 border border-zinc-800/60 text-xs space-y-1"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-zinc-200">{item.name}</span>
                      <span className="text-[9px] px-1.5 py-0.2 rounded bg-zinc-900 text-zinc-400 border border-zinc-800">
                        {item.category}
                      </span>
                    </div>

                    <div className="flex items-center gap-1">
                      <a
                        href={item.docs_url}
                        target="_blank"
                        rel="noreferrer"
                        className="p-1 text-zinc-500 hover:text-sky-400"
                        title="Документация"
                      >
                        <ExternalLink className="w-3 h-3" />
                      </a>

                      {isAdded ? (
                        <span className="text-[10px] text-emerald-400 font-medium px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-800/40">
                          ✓ Готово
                        </span>
                      ) : (
                        <button
                          onClick={() => onInstall(item.name)}
                          disabled={isInstalling}
                          className="flex items-center gap-1 px-2 py-0.5 bg-zinc-800 hover:bg-emerald-600 text-zinc-200 hover:text-white rounded text-[11px] transition-colors cursor-pointer"
                        >
                          <Download className="w-3 h-3" />
                          <span>+ Установить</span>
                        </button>
                      )}
                    </div>
                  </div>

                  <p className="text-[11px] text-zinc-400 leading-snug">
                    {item.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
