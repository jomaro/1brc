defmodule Elx.ParallelV1 do
  @moduledoc """
  Documentation for `Elx`.
  """

  def process_file(file) do
    file
    |> File.stream!(read_ahead: 16 * 1024)
    |> Flow.from_enumerable()
    |> Flow.map(fn line ->
      [station, measurement] = String.split(line, ";")

      {measurement, _} = Float.parse(measurement)

      {station, measurement}
    end)
    |> Flow.partition()
    |> Flow.reduce(fn -> %{} end, fn {station, measurement}, map ->
      default = %{
        sum: measurement,
        quantity: 1,
        min: measurement,
        max: measurement
      }

      Map.update(map, station, default, fn existing ->
        %{
          sum: existing.sum + measurement,
          quantity: existing.quantity + 1,
          min: min(existing.min, measurement),
          max: max(existing.max, measurement)
        }
      end)
    end)
    |> Enum.map(fn {station, stats} ->
      {station,
       Enum.join(
         [
           :erlang.float_to_binary(stats.min, decimals: 1),
           :erlang.float_to_binary(stats.sum / stats.quantity, decimals: 1),
           :erlang.float_to_binary(stats.max, decimals: 1)
         ],
         ","
       )}
    end)
  end
end
