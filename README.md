# PGAcloud_Initializer
Bachelor's Thesis on deploying Parallel Genetic Algorithms (PGAs) in the cloud.
This specific repository contains the **cloud initializer container**.

The *Initializer* generates the initial population if none was provided.
In order to do that, it requires knowledge about the individual's structure and should thus always be adjusted
to the problem the PGA is intended to solve.

The generated population will then be forwarded to the *Fitness* operator for an initial evaluation.

## License
*PGAcloud_Initializer* is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT).
Please see the [LICENSE](LICENSE.md) file for full details.
