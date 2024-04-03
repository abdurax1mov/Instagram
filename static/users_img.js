const img = document.querySelectorAll(".rasm")
const sel7 = document.querySelectorAll(".select7")
const x = document.querySelectorAll(".x5")
img.forEach((item, index) => {
    item.addEventListener("click", () => {
        sel7[index].classList.toggle("select1")
    })
})
x.forEach((item, index) => {
    item.addEventListener("click", () => {
        sel7[index].classList.remove("select1")
    })
})