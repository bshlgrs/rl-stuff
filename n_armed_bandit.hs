import System.Random
import Data.Array

-- this shit is hard

leverVariance = 1.0

type BanditProblem = [Float]

type ValueTable = Array Int (Float, Int)

updateValueTable :: ValueTable -> Int -> Float -> ValueTable
updateValueTable table pos newVal = let (oldAverage, numTrials) = table!pos in
            table // (pos, ((oldAverage + newVal) / (numTrials + 1), numTrials + 1))

chooseMove :: ValueTable -> Float -> [Float] -> IO Int
chooseMove table epsilon randoms = do
    ???