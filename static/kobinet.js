const img = document.querySelectorAll(".rasm")
const img1 = document.querySelectorAll(".rasm1")
const sel = document.querySelectorAll(".select")
const sel1 = document.querySelectorAll(".select1")
const x = document.querySelectorAll(".x1")
const x1 = document.querySelectorAll(".x2")
const username = document.querySelector('.username')
const sav = document.querySelector(".sa1")
const sav_flex = document.querySelector(".sava")
const foto = document.querySelector(".fo")
const foto_nome = document.querySelector(".img80")
const chi = document.querySelector(".chi3")
const chi1 = document.querySelector(".chi45")
img.forEach((item, index) => {
    item.addEventListener("click", () => {
        sel[index].classList.toggle("select2")
    })
})
img1.forEach((item, id) => {
    item.addEventListener("click", () => {
        sel1[id].classList.toggle("select3")
    })
})

x.forEach((item, id) => {
    item.addEventListener("click", () => {
        sel[id].classList.remove("select2")
    })
})
x1.forEach((item, id) => {
    item.addEventListener("click", () => {
        sel1[id].classList.remove("select3")
    })
})

sav.addEventListener("click", () => {
    chi.classList.add("none1")
    sav_flex.classList.add("display")
    foto_nome.classList.toggle("none1")
    chi1.classList.toggle("chiz46")
})

foto.addEventListener("click", () => {
    sav_flex.classList.remove("display")
    foto_nome.classList.remove("none1")
    chi.classList.remove("none1")
    chi1.classList.remove("chiz46")
})
