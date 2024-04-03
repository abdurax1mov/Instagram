const img = document.querySelectorAll(".kom")
const sel = document.querySelectorAll(".select")
const x = document.querySelectorAll(".x11")
img.forEach((item, index) => {
    item.addEventListener("click", () => {
        sel[index].classList.toggle("select1")
    })
})
x.forEach((item, index) => {
    item.addEventListener("click", () => {
        sel[index].classList.remove("select1")
    })
})