module.exports = function (source) {
    const reg = new RegExp(this.query && this.query.shebangRegExp || /[\s\n\r]*(#!.*)[\s\n\r]*/gm);
    return source.toString().replace(reg, '');
};