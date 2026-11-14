// Read data from the server
const buttons    = document.getElementById("buttons")
const questionP  = document.getElementById("question")
const jsonP      = document.getElementById("json")
const resultP    = document.getElementById("result")
const endPoint = "/ask"

buttons.addEventListener("click", treatQuery)

function treatQuery({target}) {
  const { question } = target.dataset
  questionP.textContent = `Natural language question = "${question}"`
  
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  }
  fetch(endPoint, options)
  .then(response => response.json())
  .then(displayResults)
}

function displayResults(results) {
  jsonP.textContent =  JSON.stringify(results, null, '  ')
  resultP.textContent = results.answer
}