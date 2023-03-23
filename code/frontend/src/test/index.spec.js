import {test,expect, it,fetch,vi} from "vitest"
import mockAxios from 'axios';


describe('Test function logic', () => {

 function openPaper(url) {

    let isResult = true;
    return isResult
  }

function addPaper(pdfSource) {
    console.log("start addPaper");
    const payload = {
      url: pdfSource,
    };
    mockAxios
      .post("add-paper", payload)
      .then((res) => {
        return res
      })
      .catch((error) => {
        console.log(error);
      });
  }

function getPapers() {
    console.log("start getPapers");
    const path = "library";
    mockAxios
      .get(path)
      .then((res) => {
        return res
      })
      .catch((error) => {
        console.error(error);
      });
  }
test('test result',()=>{

  expect(openPaper("https://arxiv.org/pdf/2211.17169.pdf")).toBe(true);
})

test('test result',()=>{

  expect(addPaper("https://arxiv.org/pdf/2211.17169.pdf")).toEqual(undefined);
})

test('test result',()=>{

  expect(getPapers()).toEqual(undefined);
})
})
