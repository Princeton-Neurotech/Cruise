const ShebangPlugin = require('webpack-shebang-plugin');

plugins: [
    new ShebangPlugin(),
    new webpack.BannerPlugin({ banner: "#!/usr/bin/env node", raw: true })
]
var OpenBrowserPlugin = require('open-browser-webpack-plugin');

plugins: [
  new OpenBrowserPlugin({ url: 'http://localhost:3000' })
]

