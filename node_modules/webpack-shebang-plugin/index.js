const fs = require('fs');
const path = require('path');
const { ReplaceSource } = require('webpack-sources');

module.exports = class ShebangPlugin {

    constructor(opts = {}) {
        this.entries = {};
        this.options = {
            shebangRegExp: /[\s\n\r]*(#!.*)[\s\n\r]*/gm,
            chmod: 0o755,
            ...(opts || {})
        };
        this.shebangedAssets = {};
        if (!this.options.shebangRegExp) {
            this.options.shebangRegExp = /[\s\n\r]*(#!.*)[\s\n\r]*/gm;
        }
        if (!this.options.chmod && this.options.chmod !== 0) {
            this.options.chmod = 0o755;
        }
    }

    apply(compiler) {
        compiler.hooks.entryOption.tap('ShebangPlugin', (context, entries) => {
            this.entries = {};
            this.shebangedAssets = {};
            for (const name in entries) {
                const entry = entries[name];
                let first = '';
                if (Array.isArray(entry)) {
                    first = entry[0];
                } else if (Array.isArray(entry.import)) {
                    first = entry.import[0];
                } else if (typeof entry == 'string') {
                    first = entry;
                }
                if (!first) {
                    throw new Error('Failed to find entry config. webpack@>=4.0.0 is required.');
                }
                const file = path.resolve(context, first);
                if (fs.existsSync(file)) {
                    const content = fs.readFileSync(file).toString();
                    const matches = new RegExp(this.options.shebangRegExp).exec(content);
                    if (matches && matches[1]) {
                        this.entries[name] = { shebang: matches[1] };
                    }
                }
            }
        });
        compiler.hooks.thisCompilation.tap('ShebangPlugin', compilation => {
            compilation.hooks.chunkAsset.tap('ShebangPlugin', (mod, filename) => {
                const name = mod.name;
                if (name in this.entries) {
                    this.entries[filename] = this.entries[name];
                }
            });
            compilation.hooks.buildModule.tap('ShebangPlugin', mod => {
                if (mod.loaders instanceof Array && mod.loaders.length) {
                    mod.loaders.push({
                        loader: path.resolve(__dirname, 'loader.js'),
                        options: this.options || {}
                    });
                }
            });
        });
        compiler.hooks.make.tap('ShebangPlugin', compilation => {
            compilation.hooks.afterOptimizeAssets.tap('ShebangPlugin', assets => {
                for (const name in assets) {
                    const source = assets[name];
                    if (name in this.entries) {
                        const { shebang } = this.entries[name];
                        const rep = new ReplaceSource(source, 'shebang');
                        rep.insert(0, shebang + '\n\n', 'shebang');
                        compilation.updateAsset(name, rep);
                        this.shebangedAssets[name] = shebang;
                    }
                }
            });
        });
        compiler.hooks.assetEmitted.tap('ShebangPlugin', (file, { targetPath }) => {
            let target = targetPath;
            if (!target && compiler.outputPath) {
                target = path.resolve(compiler.outputPath, file);
            }
            if (this.options.chmod !== 0) {
                if (!target) {
                    throw new Error('Failed to locate the output file. webpack@>=4.0.0 is required.');
                }
                if (file in this.shebangedAssets) {
                    fs.chmodSync(target, this.options.chmod);
                }
            }
        });
    }
}
