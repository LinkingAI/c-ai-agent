const hre = require("hardhat");
require("dotenv").config();

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("👉 Wallet usada:", deployer.address);

  const ContractFactory = await hre.ethers.getContractFactory("AIInvestmentLog");
  const contract = await ContractFactory.deploy();

  await contract.waitForDeployment(); // ✅ para Hardhat + Ethers v6+

  console.log("✅ Contrato desplegado en:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
