# 🪙 Cambio de Billetes a Monedas

## 💡 Descripción del Problema

Un cliente desea cambiar una cantidad de dinero que posee en **billetes** por la misma cantidad equivalente en **monedas**. El objetivo principal es que el cambio se realice utilizando la **menor cantidad posible de monedas**.

---

## 🔍 Ejemplos

### Ejemplo 1: Cantidad de $45

* **Cantidad Entregada:** 45 en billetes.
* **Denominaciones de Moneda Disponibles:** `[1, 5, 10, 25, 50]`
* **Cambio Óptimo:** Se le dará al cliente **tres (3)** monedas: dos monedas de **10** y una moneda de **25**.
    * **Resultado:** `[10, 10, 25]`

### Ejemplo 2: Cantidad de $50

* **Cantidad Entregada:** 50 en billetes.
* **Denominaciones de Moneda Disponibles:** `[1, 5, 10, 25, 50]`
* **Cambio Óptimo:** Se le dará al cliente **dos (2)** monedas de **25**.
    * **Resultado:** `[25, 25]`