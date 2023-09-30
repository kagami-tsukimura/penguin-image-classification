# The Types in TypeScript

## What are types?

-   A **type** is a resusable set of rules.
-   A type may have **properties** and **functions**
-   It ca use reused over and over again.
-   By reused a **type** means you arecreating an **instance** of it.
-   In typeScript, the most imporatnt items is the **type**

## How does **types** work?

We know JavaScript have types such as Number, string, Boolean, array and many others. But when you write JS code you don't declare explicitly the types of aby items, it is set during runtime. The problem is we don;t have any control over the it. So, when a bug detected we don't know for which types are in problem. And in TypeScript, you can also set your own **type**s.

Important:

-   In TypeScript(TS), name of the type is not important but the shape of it.

## Types

### The **any** type

-   The **any** types is a dynamic type that can be set to any other type.
-   **any** type can be set to anything or reset to anything.
-   Compiler will not check it for you. means, during development it will not provide you with any warning regarding the variable.
-   So, if possible avoid **any** type. - **WHEN To USE** - In large application, It depends on multiple languages, external data so, it can't be possible to know every types the application will get then **any** will be the savior or escape hatch.

Practice code in Playground
[**any** type example](https://www.typescriptlang.org/play?#code/DYUwLgBAtgngcgQyiAXBBA7GEC8EBEAggG4CWAVqWPgFA0DGA9hgM6OgB0wjA5gBSxEyAJR1BSELggBGAEwBmACwBWOk1bsQXXgPgTRNccikYQAdwiEATlYQw+oo1oAOAVxYALPvgAqMZ5IwjK4QGBIQHiBWWvii6myc3PxOwkA)

### The **unknown** type

-
