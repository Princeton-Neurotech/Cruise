const ShebangPlugin = require('webpack-shebang-plugin');

plugins: [
    new ShebangPlugin(),
    new webpack.BannerPlugin({ banner: "#!/usr/bin/env node", raw: true })
]

