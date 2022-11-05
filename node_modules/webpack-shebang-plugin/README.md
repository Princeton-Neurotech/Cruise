# Introduction

This is an all-in-one webpack plugin which prepends hashbangs automatically to the generated bundle files and make it executable -- all revived from your entry source file.

*You can actually use this plugin to do anything that BannerPlugin is able to do, by changing the default pattern and the mark in your source files. Please see **More Usage** demo for more details.*

This plugin embeds a simple loader which deals with the hashbang syntax OR any syntax you can specify as a regular expression. You don't need any other dependencies or libs, such as shebang-loader, BannerPlugin, nor do you need extra configurations.

# Requirements

webpack >= 4.0.0 is required.

# Installation

In npm:
```
npm install -D webpack-shebang-plugin
```
Or in yarn:
```
yarn add -D webpack-shebang-plugin
```

# Simple Usage

#### Entry JS file:

``` javascript

#!/usr/bin/env node

// The first line is the shebang you want be added.
// Don't worry about the spaces and line breaks around it.

// You can add shebang mark anywhere in any source file,
// but only if the first meaningful line of your entry file matches the pattern,
// it will be regarded as the shebang and will be prepended to the output bundle,
// all the other useless shebang marks will be removed in the output.
console.log('this is your entry JS file.');

```

---

#### webpack.config.js:

``` javascript

const ShebangPlugin = require('webpack-shebang-plugin');

// ...other webpack configuration

plugins: [
    // ...other webpack plugins

    new ShebangPlugin()

    // ...other webpack plugins
]

// ...other webpack configuration
```

---

#### The output bundle looks like:

``` javascript
#!/usr/bin/env node

/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({
/*
  ...... generated code ......
 */
```

# Configuration

``` javascript
new ShebangPlugin({
    // optional, you can specify a different regular expression here for your own pattern.
    // the pattern below is used by default, if unset. It matches syntax like:
    //      #!........
    // The regular expression should contain a group of the main shebang part as $1, in the above case,
    // the shebang part "#!........" will be grouped out.
    // * If you create one of your own, you should keep sure that the main part will be grouped out as $1,
    //   and it will be used as your shebang.
    // * If you are not sure how to write your regular expression, please just leave it unset.
    shebangRegExp: /[\s\n\r]*(#!.*)[\s\n\r]*/gm,

    // optional, you can specify r/w/e permissions in octal value.
    // The default value is 0o755, which makes the output bundle executable.
    // You can set the value to 0, if you want to keep the default permissions.
    chmod: 0o755,
})
```

# More Usage

### To use this plugin as a general banner plugin purpose:

Suppose you have two different entries, and you wish to have two output bundles:

- **dist/**
    - *bundle1.js*
    - *bundle2.js*
- **src/**
    - *entry1.js*
    - *entry2.js*
    - *import-in-first-bundle.js*
- *webpack.config.js*

#### src/entry1.js

``` javascript
/***
This is my custom banner
I want this block appear
in my first bundle.
***/

require('./required-by-entry1.js');

console.log('my first bundle');
```

#### src/import-in-first-bundle.js

``` javascript
/***
This block also matches the
custom banner pattern, but
because this file is not the entry
asset, so this block of content
will be abandoned.
***/

console.log('imported in first bundle');
```

#### src/entry2.js

``` javascript
console.log('my second bundle');
```

#### webpack.config.js

``` javascript
const path = require('path');
const ShebangPlugin = require('webpack-shebang-plugin');

module.exports = {
    mode: 'production',
    target: 'node',
    entry: {
        first: {
            import: ['./src/entry1.js', './src/import-in-first-bundle.js'],
            filename: 'bundle1.js'
        },
        second: {
            import: './src/entry2.js',
            filename: 'bundle2.js'
        },
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: [
                    /node_modules/
                ],
                use: [
                    {
                        loader: 'babel-loader'
                    }
                ]
            }
        ]
    },
    plugins: [
        new ShebangPlugin({
            shebangRegExp: /[\s\n\r]*(\/\*{3}[\s\S]*?\*{3}\/)[\s\n\r]*/gm
        })
    ]
}
```

### The dist files look like:

#### dist/bundle1.js

``` javascript
/***
This is my custom banner
I want this block appear
in my first bundle.
***/
// entry1.js code here
// import-in-first-bundle.js code here
```

#### dist/bundle2.js

``` javascript
// entry2.js code here
```

# Author

qiangyizhou@bilibili.com
