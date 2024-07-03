import "./style.css";

import * as monaco from "monaco-editor/esm/vs/editor/editor.api";
import "monaco-editor/esm/vs/basic-languages/cpp/cpp.contribution";

import diff_match_patch from "diff-match-patch";
import { createTwoFilesPatch } from "diff";
import { Diff2HtmlUI } from "diff2html/lib/ui/js/diff2html-ui";
import "diff2html/bundles/css/diff2html.min.css";

const editorElem = document.getElementById("editor");
const codeElem = document.getElementById("code");
const formElem = document.getElementById("form-codegolf");
const charsElem = document.getElementById("chars");
const expectedElem = document.getElementById("expected");
const outputElem = document.getElementById("output");
const diffElem = document.getElementById("diff");

const editor = monaco.editor.create(editorElem, {
  value: `#include <iostream>

int main(int argc, char* argv[]) {
    // Printing
    std::cout<<"Hello, World!"<<std::endl;

    // Looping
    for (int i = 0; i < 10; i++)
        std::cout<<i<<std::endl;

    // Accessing arguments
    for (int i = 1; i < argc; i++)
        std::cout<<argv[i]<<std::endl;

    return 0;
}

// Code is compiled with clang with -std=c++2b
// See: https://clang.llvm.org/cxx_status.html`,
  language: "cpp",
  codeLens: false,
  contextmenu: false,
  minimap: {
    enabled: false,
  },
  scrollBeyondLastLine: false,
  scrollbar: {
    alwaysConsumeMouseWheel: false,
  },
});

const code = editor.getModel().getValue();
codeElem.value = code;
charsElem.textContent = code.trim().replace(/(\r\n|\n|\r)/gm, "").length;

editor.getModel().onDidChangeContent((e) => {
  const code = editor.getModel().getValue();
  codeElem.value = code;
  charsElem.textContent = code.trim().replace(/(\r\n|\n|\r)/gm, "").length;
});

formElem.addEventListener("submit", (e) => {
  e.preventDefault();
  const fields = formElem.elements;
  const formData = {
    code: fields["code"].value,
    code_lang: fields["code_lang"].value,
  };

  fetch(window.location.href, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': fields["csrfmiddlewaretoken"].value
    },
    body: JSON.stringify(formData)
  })
  .then((res) => { return res.json() })
  .then((res) => {
    const expected = res.expectedOutput.replace(/\r\n/g, "\n");
    const actual = res.userOutput.replace(/\r\n/g, "\n");

    // Создание unified diff с помощью библиотеки diff
    const diffText = createTwoFilesPatch(
      "expected.txt",
      "actual.txt",
      expected,
      actual
    );

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
      document.querySelectorAll(".d2h-diff-tbody").forEach(a => a.querySelector("tr")?.remove())
    }

    expectedElem.textContent = res.expectedOutput;
    outputElem.textContent = res.userOutput;
  });
});
