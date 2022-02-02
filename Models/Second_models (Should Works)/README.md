Those models were made following the procedure proposed by Y. Mehta in his article
"Bottom-Up and Top-Down: Predicting Personality with Psycholinguistic and Language Model Features"

available at:
https://sentic.net/predicting-personality-with-psycholinguistic-and-language-model-features.pdf
or on the GitHub page:
https://github.com/yashsmehta/personality-prediction

They are produce with the MLP_LM.py file, which are, accordingly to the paper, the best performing models for every
OCEAN's traits except the NEUROTICISM.
Those were saved using the from_logits=FALSE arguments during their training phases.

the value between parenthesis are the VAL_ACC calculated during the training phase.
For exemple,
Model_AGR(6301) had 63.01% accuracy on the validation dataset

Those models were the ones used in this work.