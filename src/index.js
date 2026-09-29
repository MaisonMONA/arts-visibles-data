import { readFile, writeFile } from "node:fs/promises";

const travail = JSON.parse(
  await readFile(makePath("lieu-travail_qc"), "utf8")
);

const residence = JSON.parse(
  await readFile(makePath("lieu-residence_qc"), "utf8")
);

const naissance = JSON.parse(
  await readFile(makePath("lieu-naissance_qc"), "utf8")
);

const lieuDeTravailPlat = applatirSparql(travail);
const lieuDeNaissancePlat = applatirSparql(naissance);
const lieuDeResidencePlat = applatirSparql(residence);

// console.log(
//   lieuDeNaissancePlat,
//   lieuDeResidencePlat,
//   lieuDeTravailPlat
// )

const mergedResults = fusionnerParQidNom(
  lieuDeNaissancePlat,
  lieuDeResidencePlat,
  lieuDeTravailPlat
);

console.log(mergedResults);

// throw new Error("STOP")

await writeFile(
  "./_assets/artistes.json",
  JSON.stringify(mergedResults, null, 2),
  "utf8"
);

const headers = Object.keys(mergedResults[0]);

const csv = [
  headers.join(","),
  ...mergedResults.map(row =>
    headers.map(header =>
      JSON.stringify(row[header] ?? "")
    ).join(",")
  )
].join("\n");

await writeFile("./_assets/artistes.csv", csv, "utf8");

// fonctions

function makePath(segment) {
  return `./data/artiste/${segment}/results.json`
}

function applatirSparql(data) {
  return data.results.bindings.map(binding =>
    Object.fromEntries(
      Object.entries(binding).map(([key, value]) => [
        key,
        value.value
      ])
    )
  );
}

function fusionnerParQidNom(...datasets) {
  return Object.values(
    datasets.flat().reduce((acc, item) => {
      const key = JSON.stringify([item.artiste, item.nom]); // attention au `:`

      acc[key] = {
        ...acc[key],
        ...item
      };

      return acc;
    }, {})
  ).map(item => ({
    ...item,
    naissance: item.naissance ?? "",
    lieu_travail: item.lieu_travail ?? "",
    residence: item.residence ?? ""
  }));
}