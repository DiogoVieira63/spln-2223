## TPC

Normalizar Json
Construir ply para gramática

---
-Indice: 636
-Area: [Terapeutica]
-Nota: String
es :  []
+atributo: valor

dicionario -> meta entrada*

meta -> 
entrada -> item*
item -> at-conceito
      | lingua
at-conceito-> id ':' valor
lingua -> id_lingua ':' t*
t -> termo at-termo*
at-termo -> '+' id ':' valor

