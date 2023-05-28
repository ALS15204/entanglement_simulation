<!-- PROJECT LOGO -->
<h3 align="center">Entanglement Forging simulation with water molecule</h3>
  <p align="center">
    Simulate water ground state energy with entanglement forging in VQE
  </p>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#todos">TODOs</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This repository is prepared to reproduce the results discussed in the paper ["Doubling the size of quantum simulators by entanglement forging"](https://arxiv.org/pdf/2104.10220.pdf) by Andrew Eddins et al.

The repository focuses on reproducing Fig 3b and 4b of the paper. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started
Follow the steps below to get set up the project
1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Set up venv wih Python 3.9
   ```
   python3.9 -m venv venv
   ```
3. Activate venv
   ```
   source venv/bin/activate
   ```
4. Install requirements
   ```
   pip install -e .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

A demonstration of my experiment can be found in the python notebook [[water_simulation_case_b.ipynb](notebooks%2Fwater_simulation_case_b.ipynb)].

To reproduce what has been discussed in the notebook, follow the steps below:

1. Run the following command to produce simulated water molecule data.
   ```sh
   python3.9 -m entanglement_simulation.water_molecule
   ```
   This will create the [[water_data_case_b.json](entanglement_simulation%2Fdata%2Fwater_data_case_b.json)]
2. Run the following command to search the best results through hyperparameters.
   ```sh
   python3.9 -m entanglement_simulation.scripts.entangelement_forge
   ```
   This will prepare the experiment folder [case_b_reduced_orbitals_0_3_k3](experiments%2Fcase_b_reduced_orbitals_0_3_k3)
3. Finally, run the following command to make plots.
   ```sh
   python3.9 -m entanglement_simulation.scripts.make_plots
   ```
   This will create the plots in the [plots](experiments%2Fcase_b_reduced_orbitals_0_3_k3%2Fplots) folder.

[NOTE] Out of curiosity, I have applied the best hyperparameters found in case b to case a and case c. The results are shown in the notebook:
* [[simulate_case_a.ipynb](notebooks%2Fsimulate_case_a.ipynb)]. Case A plots: [[plots](experiments%2Fcase_a_reduced_orbitals_0_3_k3%2Fplots)].
* [[simulate_case_c.ipynb](notebooks%2Fsimulate_case_c.ipynb)]. Case C plots: [[plots](experiments%2Fcase_c_reduced_orbitals_0_3_k3%2Fplots)].

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- TODOS -->
## TODOs

- [ ] Add tests: due to time limitation, I did not add tests for this project. I will add tests in the future.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ronin Wu - [@RoninWu](https://twitter.com/RoninWu) - roninwu@gmail.com

Project Link: [https://github.com/ALS15204/entanglement_simulation](https://github.com/ALS15204/entanglement_simulation)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* I sincerely thank Dr. Andrew Eddins for giving [a very comprehensive talk](https://www.youtube.com/watch?v=vJZRUf1abQs) on his work. I learned a lot from his talk and the paper.
* The implementation in this work has referenced the blogpost [Try Out the Latest Advances in Quantum Computing With Prototypes](https://medium.com/qiskit/try-out-the-latest-advances-in-quantum-computing-with-ibm-quantum-prototypes-11f51124cb61). I sincerely thank the authors for providing comprehensive examples and tutorials.
* Special thanks to my dear friend Dr. Valentin Stauber, who has provided me fruitful discussions and suggestions on this project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
