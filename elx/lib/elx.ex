defmodule Elx do
  @moduledoc """
  Documentation for `Elx`.
  """

  alias Elx.SerialV1
  alias Elx.ParallelV1

  def serial_v1(file) do
    process(file, &SerialV1.process_file/1)
  end

  def parallel_v1(file) do
    process(file, &ParallelV1.process_file/1)
  end

  defp process(file, func) do
    start = :os.system_time(:millisecond)

    file = "../#{file}.txt"

    func.(file)
    |> IO.inspect()

    IO.inspect(:os.system_time(:millisecond) - start, label: "Timing")
  end
end
