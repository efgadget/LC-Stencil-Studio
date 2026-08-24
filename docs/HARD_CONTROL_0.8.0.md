# LC Stencil Studio 0.8.0 — Hard Control

Checkpoint funzionale del 24/08/2026.

## Verificato manualmente
- Creazione nuovo progetto
- Importazione immagine
- Modifica X/Y
- Ridimensionamento con proporzioni
- Rotazione
- Salvataggio progetto .lcs
- Avviso modifiche non salvate
- Chiusura e riapertura progetto
- Ripristino di immagine e geometria salvata

## Criticità individuate
1. La duplicazione crea più elementi sul canvas, mentre il formato progetto salva una sola immagine/geometria.
2. Eliminando l'immagine, il salvataggio può conservare il precedente image_path.
3. La centratura usa scene.itemsBoundingRect() invece del solo rettangolo materiale.
4. Versione interna canvas.py ancora indicata come 0.7.0.
5. Il progetto dipende dal percorso esterno dell'immagine originale: spostamento/rinomina/cancellazione può impedirne il ripristino.
6. Dirty-state da sottoporre a test distruttivo completo.

## Regola di stabilità
Le funzioni CAD già validate (X/Y, dimensionamento, rotazione, proporzioni, salvataggio e riapertura) non devono regredire durante le correzioni.
