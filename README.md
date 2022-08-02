# Thesis-PairwiseRanking-WebApp

Projekt do pracy dyplomowej (inżynierskiej), znajdującej się [tutaj](https://drive.google.com/file/d/1GAXih2-AP05_K60uHtzlSDPZrHcbEjV_/view?usp=sharing).

## Opis projektu

Gdy ludzie dokonują subiektywnych ocen za pomocą liczb wyrażonych w określonej skali, istnieje zjawisko, gdzie dystrybucja ocen jest nieproporcjonalnie skupiona na najwyższych wartościach. Powoduje to utratę wartości informacyjnej tych ocen.

Jednym z rozwiązań tego problemu jest porównywanie elementów parami. Jest to metoda umożliwiająca większą dokładność, gdyż upraszcza ona problem, do określenia który element z dwóch jest bardziej wartościowy. Ocena elementu kolekcji w skali, przykładowo, 1 do 10, wymaga by określić pozycję danego elementu w kontekście całej kolekcji, która może zawierać tysiące elementów. Posiadając listę takich porównań, można zastosować modele matematyczne jak Bradley-Terry, by uzyskać komparatywne oceny elementów w ramach tej kolekcji.

Szeregując elementy na podstawie tychże ocen, możliwym jest uzyskanie wiarygodnego rankingu (wg. preferencji użytkownika) tych elementów. W taki sposób funkcjonuje m.in. ranking szachowy Elo, czy systemy matchmakingowe w niektórych kompetytywnych grach e-sportowych.

Projekt ten umożliwia ocenę parami elementów wybranych kolekcji mediów. Zaimplementowane są na chwilę obecną przykładowe źródła danych Anilist i Steam (gry przypisane do danego konta).

Projekt jest aplikacją webową, rozdzieloną na REST Web API wykonane w Pythonowym frameworku Flask oraz klienta tegoż API wykonanego w Vue.js.


----------------------------------

## Compilation/Running

To run frontend & backend on NixOS (assuming git is installed):
```bash
 $ git clone https://github.com/Sinity/pwrank.git
 $ cd pwrank
 $ nix-shell
   # necessary only once after cloning, unless dependencies change
 $ (cd frontend && npm install) 
 $ (cd frontend && npm run serve) &
 $ python backend/webrankit/app.py
```
