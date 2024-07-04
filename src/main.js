import "./style.css";

import { createTwoFilesPatch } from "diff";
import { Diff2HtmlUI } from "diff2html/lib/ui/js/diff2html-ui";
import "diff2html/bundles/css/diff2html.min.css";

import { basicSetup, EditorView } from "codemirror";
import { EditorState, Compartment } from "@codemirror/state";
import { python } from "@codemirror/lang-python";
import { javascript } from "@codemirror/lang-javascript";
import { cpp } from "@codemirror/lang-cpp";
import { oneDark } from "@codemirror/theme-one-dark";

const editorElem = document.getElementById("editor");
const codeElem = document.getElementById("code");
const langElem = document.getElementById("code_lang");
const formElem = document.getElementById("form-codegolf");
const submitElem = document.getElementById("submit");
const charsElem = document.getElementById("chars");
const expectedElem = document.getElementById("expected");
const outputElem = document.getElementById("output");
const diffElem = document.getElementById("diff");
const sectionOutputElem = document.getElementById("section-output");
const sectionOutputMessage = document.getElementById("output-message");

let language = new Compartment(),
  tabSize = new Compartment();

const themeConfig = new Compartment();

let state = EditorState.create({
  doc: `#include <iostream>

int main(int argc, char* argv[]) {
    // Printing
    std::cout<<"Hello, World!"<<std::endl;
}`,
  extensions: [
    basicSetup,
    language.of(cpp()),
    tabSize.of(EditorState.tabSize.of(4)),
    oneDark,

    EditorView.updateListener.of(function (e) {
      if (e.docChanged) {
        const text = e.state.doc.toString().trim();

        codeElem.value = text;
        charsElem.textContent = text.length || 0;
      }
    }),
  ],
});

let view = new EditorView({
  state,
  parent: editorElem,
});

charsElem.textContent = state.doc.toString().trim().length || 0;
codeElem.value = state.doc.toString();

window.addEventListener("keydown", function (event) {
  if (event.ctrlKey && event.key === "Enter") {
    event.preventDefault();

    submitElem.click();
  }
});

// editorElem.addEventListener("keydown", function (event) {
//   if (event.ctrlKey && event.key === "Enter") {
//     event.preventDefault();

//     submitElem.click();
//   }
// });

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
  codeElem.value = view.state.doc.toString();

  sendForm(e);
});

setScoreboard();
setInterval(() => {
  setScoreboard();
}, 5000);

function setScoreboard() {
  fetch(window.location.href + "get_scoreboard/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      document.getElementById("scoreboard").innerHTML = data.html;
    })
    .catch((error) => {
      console.error("Error", error);
    });
}

const username = localStorage.getItem("username") || "";
document.getElementById("username").value = username;

function sendForm(e) {
  e.preventDefault();

  const fields = formElem.elements;

  const username = fields["username"].value;

  const formData = {
    code: fields["code"].value.trim(),
    code_lang: fields["code_lang"].value,
    username:
      username + "#" + document.getElementById("sessid").textContent.trim(),
    code_len: state.doc.toString().trim().length,
  };

  localStorage.setItem("username", username);

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
      const expected = res.expectedOutput.replace(/\r\n/g, "\n").trim();
      const actual = res.userOutput.replace(/\r\n/g, "\n").trim();

      console.log(expected);
      console.log(actual);

      // Создание unified diff с помощью библиотеки diff
      const diffText = createTwoFilesPatch(
        "expected.txt",
        "actual.txt",
        actual,
        expected
      );

      if (res.is_correct) {
        diffElem.textContent = "Полное совпадение, юху!";

        sectionOutputMessage.textContent = "ВЫ МОЛОДЦЫ! с:";
        sectionOutputMessage.classList.remove("error");
        sectionOutputMessage.classList.add("success");
      } else {
        sectionOutputMessage.textContent = "Увы :с";
        sectionOutputMessage.classList.add("error");
        sectionOutputMessage.classList.remove("success");

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

      sectionOutputElem.style.display = "block";
      sectionOutputElem.scrollIntoView(true);
    });
}
