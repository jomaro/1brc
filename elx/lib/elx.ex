defmodule Elx do
  @moduledoc """
  Documentation for `Elx`.
  """

  # time: 1487357
  def version1(file) do
    start = :os.system_time(:millisecond)

    "../#{file}.txt"
    |> File.stream!(read_ahead: 16*1024)
    |> Stream.map(fn line ->
      [station, measurement] = String.split(line, ";")

      {measurement, _} = Float.parse(measurement)

      {station, measurement}
    end)
    |> Enum.reduce(%{}, fn {station, measurement}, map ->
      default = %{
        sum: measurement,
        quantity: 1,
        min: measurement,
        max: measurement,
      }

      Map.update(map, station, default,
        fn existing ->
          %{
            sum: existing.sum + measurement,
            quantity: existing.quantity + 1,
            min: min(existing.min, measurement),
            max: max(existing.max, measurement),
          }
        end)
    end)
    |> Enum.map(fn {station, stats} ->
      {station, Enum.join([
        :erlang.float_to_binary(stats.min, [decimals: 1]),
        :erlang.float_to_binary(stats.sum / stats.quantity, [decimals: 1]),
        :erlang.float_to_binary(stats.max, [decimals: 1]),
      ], ",")}
    end)
    |> IO.inspect()

    :os.system_time(:millisecond) - start
  end
end
