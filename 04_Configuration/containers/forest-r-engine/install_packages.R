# Forest OS: R Engine Package Installation Script
# Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)

# Configure repositories preserving P3M binary cache and adding verified R-Universe endpoints
current_repos <- getOption("repos")
options(repos = c(
  rlidar = "https://r-lidar.r-universe.dev",
  carlos = "https://carlos-alberto-silva.r-universe.dev",
  current_repos
))

cat("======================================================================\n")
cat(" Forest OS: Active Package Repositories\n")
cat("======================================================================\n")
print(getOption("repos"))

# Primary binary and standard CRAN/R-Universe dependencies
base_packages <- c(
  "remotes",
  "data.table",
  "hdf5r",
  "rlas",
  "lidR",
  "rGEDI",
  "dplR",
  "BIOMASS",
  "ForestTools",
  "hemispheR",
  "treeclim"
)

cat("======================================================================\n")
cat(" Forest OS: Installing Core Scientific Packages\n")
cat("======================================================================\n")

for (pkg in base_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("Installing: %s\n", pkg))
    install.packages(pkg, dependencies = c("Depends", "Imports", "LinkingTo"))
  } else {
    cat(sprintf("Already satisfied: %s\n", pkg))
  }
}

cat("======================================================================\n")
cat(" Forest OS: Installing Upstream GitHub Packages (TreeLS, allodb)\n")
cat("======================================================================\n")

if (!requireNamespace("TreeLS", quietly = TRUE)) {
  cat("Installing TreeLS from GitHub tiagodc/TreeLS...\n")
  remotes::install_github("tiagodc/TreeLS", upgrade = "never")
}

if (!requireNamespace("allodb", quietly = TRUE)) {
  cat("Installing allodb from GitHub forestgeo/allodb...\n")
  remotes::install_github("forestgeo/allodb", upgrade = "never")
}

cat("======================================================================\n")
cat(" Forest OS: Verification of Installed R Engine Packages\n")
cat("======================================================================\n")

target_packages <- c(
  "lidR",
  "TreeLS",
  "rGEDI",
  "BIOMASS",
  "dplR",
  "allodb",
  "ForestTools",
  "hemispheR",
  "treeclim"
)

failed <- character(0)

for (pkg in target_packages) {
  loaded <- suppressWarnings(suppressPackageStartupMessages(require(pkg, character.only = TRUE)))
  if (loaded) {
    ver <- as.character(packageVersion(pkg))
    cat(sprintf("  [PASS] %-15s v%s\n", pkg, ver))
  } else {
    cat(sprintf("  [FAIL] %-15s failed to load\n", pkg))
    failed <- c(failed, pkg)
  }
}

if (length(failed) > 0) {
  cat("\nInstallation failed for the following packages:\n")
  cat(paste(" -", failed, collapse = "\n"), "\n")
  quit(status = 1)
} else {
  cat("\nAll Forest OS R scientific packages verified successfully.\n")
  quit(status = 0)
}
