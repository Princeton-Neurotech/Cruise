# `reportValidity()` ponyfill

[GitHub](https://github.com/jelmerdemaat/report-validity) | [NPM](https://www.npmjs.com/package/report-validity) | [Demo](https://report-validity.now.sh) | [Twitter](https://twitter.com/jelmerdemaat)

This [ponyfill](https://ponyfill.com) recreates the `reportValidity` function in non-supporting browsers, and uses the native function if available.

Explanation of `reportValidity`:

> The HTMLFormElement.reportValidity() method returns true if the element's child controls satisfy their validation constraints. When false is returned, cancelable invalid events are fired for each invalid child and validation problems are reported to the user.

Source: [MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/reportValidity)

What this means in the most common use case, is that you can _programmatically call_ `reportValidity()` on a form, and it will initiate the HTML5 form validation _without submitting the form_. This often includes focussing on the first invalid field, scrolling to it, and displaying an error message (depending on the browser).

Browser support for `reportValidity` is mainly lacking in IE11: https://www.caniuse.com/#feat=constraint-validation

## Working example

See the [demo](https://report-validity.now.sh).

## Usage

Install via NPM:

```sh
npm install --save report-validity
```

Or include the UMD file in your page:

```html
<script src="report-validity.umd.js"></script>
```

After that, call the `reportValidity()` function at any time:

```js
// When using NPM, import the function:
import reportValidity from 'report-validity';

let form = document.querySelector('form'),
    btn = document.querySelector('.reportFormValidityWhenIClickThis');

btn.addEventListener('click', () => {
    // Let the browser report the validity:
    let result = reportValidity(form);
    // `result` is now true or false depending on the validity
});
```
