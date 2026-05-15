# Physics labs

## About

You can find [here](https://hsse-physics-labs.tadpole-sirius.ts.net) the interactive labs (experiment simulations), play with parameters and enjoy materialized results!

Each page represents a separate lab, where you can find experiment description, limits of applicability, and the
playground itself.


## Contents

Try out interactive labs **right now**, on our [website](https://hsse-physics-labs.tadpole-sirius.ts.net)!

_Autumn semester:_

- **M1. Throw a rock** · [General information](labs/throw_a_rock) · [Tests](tests/throw_a_rock)
- **M2. Flight to Mars** · [General information](labs/flight_to_mars) · [Tests](tests/flight_to_mars)
- **M4. Roll the ball** · [General information](labs/roll_the_ball) · [Tests](tests/roll_the_ball)
- **M5. Swing the pendulum** · [General information](labs/swing_the_pendulum) · [Tests](tests/swing_the_pendulum)

_Spring semester:_

- **M1. The capacitor** · [General information](labs/the_capacitor) · [Tests](tests/the_capacitor)
- **M3. Magnetic trap** · [General information](labs/magnetic_trap) · [Tests](tests/magnetic_trap)
- **M5. Tunnel diode oscillator** · [General information](labs/tunnel_diode_oscillator) · [Tests](tests/tunnel_diode_oscillator)
- **M10. Interference** · [General information](labs/interference) · [Tests](tests/interference)


## Launch guide

### Option 1. `uv`

Install [uv](https://docs.astral.sh/uv/) via `curl`:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

...or via `brew`:

```shell
brew install uv
```

Then, sync python dependencies:

```shell
uv sync --no-dev
```

And launch the app:

```shell
uv run streamlit run main.py
```

### Option 2. `pip`

If you don't want to install `uv`, you can use `pip` with `requirements.txt`.

Install dependencies (preferably into a virtual environment):

```shell
pip install -r requirements.txt
```

And run the app:

```shell
streamlit run main.py
```

## Research guide

If you want to learn experiments in jupyter notebooks.

```shell
uv sync --group research
```

Run jupyter notebook server from the root project dir. This will yield connection link in the terminal. Then, you can run experiments in any notebook `tests/<lab>/*`

```shell
uv run jupyter notebook --autoreload --no-browser
```

Open any `.ipynb` file in your IDE and setup a kernel using option "use existing jupyter server". Pass the connection link here.

If you are strugling with running the notebook – simply move it to the project root and try again!

## Development guide

```shell
uv sync
```

Initialize pre-commit for convenient codestyle auto-formatting:

```shell
uv run pre-commit install
```

And run the app (with hot-reload):

```shell
uv run streamlit run main.py
```
