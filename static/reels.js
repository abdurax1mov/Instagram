const img = document.querySelectorAll(".img1")
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