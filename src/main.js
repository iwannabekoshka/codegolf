import "./style.css";

import { createTwoFilesPatch } from "diff";
import { Diff2HtmlUI } from "diff2html/lib/ui/js/diff2html-ui";
import "diff2html/bundles/css/diff2html.min.css";

import { basicSetup, EditorView } from "codemirror";
import { EditorState, Compartment } from "@codemirror/state";
import { python } from "@codemirror/lang-python";
import { javascript } from "@codemirror/lang-javascript";

const editorElem = document.getElementById("editor");
const codeElem = document.getElementById("code");
const langElem = document.getElementById("code_lang");
const formElem = document.getElementById("form-codegolf");
const charsElem = document.getElementById("chars");
const expectedElem = document.getElementById("expected");
const outputElem = document.getElementById("output");
const diffElem = document.getElementById("diff");

let language = new Compartment(),
  tabSize = new Compartment();

let state = EditorState.create({
  extensions: [
    basicSetup,
    language.of(python()),
    tabSize.of(EditorState.tabSize.of(4)),

    EditorView.updateListener.of(function(e) {
      if (e.docChanged) {
        const text = e.state.doc.toString().trim();

        codeElem.value = text;
        charsElem.textContent = text.length;
      } 
  })
  ],
});

let view = new EditorView({
  state,
  parent: editorElem,
});

langElem.addEventListener("change", (e) => {
  let lang;
  if (e.target.value === "python") {
    lang = python();
  } else if (e.target.value === "javascript") {
    lang = javascript();
  }

  if (lang) {
    view.dispatch({
      effects: language.reconfigure(lang),
    });
  }
});

formElem.addEventListener("submit", (e) => {
  e.preventDefault();

  // codeElem.value = view.state.doc.toString();

  const fields = formElem.elements;
  const formData = {
    code: fields["code"].value.trim(),
    code_lang: fields["code_lang"].value,
  };

  fetch(window.location.href, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": fields["csrfmiddlewaretoken"].value,
    },
    body: JSON.stringify(formData),
  })
    .then((res) => {
      return res.json();
    })
    .then((res) => {
      const expected = res.expectedOutput.replace(/\r\n/g, "\n");
      const actual = res.userOutput.replace(/\r\n/g, "\n");

      // Создание unified diff с помощью библиотеки diff
      const diffText = createTwoFilesPatch(
        "expected.txt",
        "actual.txt",
        actual,
        expected
      );

      // TODO Эта проверка - отстой, но это лучшее что я придумал за 5 секунд
      if (!diffText.includes("@@")) {
        diffElem.textContent = "Полное совпадение, юху!";
      } else {
        const configuration = {
          drawFileList: false,
          matching: "lines",
          outputFormat: "side-by-side",
        };

        const diff2htmlUi = new Diff2HtmlUI(diffElem, diffText, configuration);
        diff2htmlUi.draw();

        document.querySelector(".d2h-file-header")?.remove();
        document
          .querySelectorAll(".d2h-diff-tbody")
          .forEach((a) => a.querySelector("tr")?.remove());
      }

      expectedElem.textContent = res.expectedOutput;
      outputElem.textContent = res.userOutput;
    });
});
