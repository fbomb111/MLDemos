async function getHelloWorld() {
    const res = await fetch('/index')
    const json = await res.text()
    console.log(JSON.stringify(json))
}

getHelloWorld()