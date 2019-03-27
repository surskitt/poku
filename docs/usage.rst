=====
Usage
=====

.. code-block:: shell

   [-h] [-c CONFIG] --consumer CONSUMER [--access ACCESS]

   -c CONFIG, --config CONFIG    config file path
   --consumer CONSUMER           pocket consumer key
   --access ACCESS               pocket access key

The app will generate an access token on first run, pass this on subsequent runs. Alternatively, enter both options into the applications config file, found at `$HOME/.config/poku.cfg`.

The config file format is detailed on the `configargparse`_ docs.

.. _configargparse: https://github.com/bw2/ConfigArgParse#config-file-syntax
