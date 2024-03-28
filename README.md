# wu-epistemic-advantage
A model of the epistemic advantage at the margins

## Questions
What are the average_cumulative_payoff lists used for?
When do I update the node's belief? Should I update it on the evidence, then on its neighbors beliefs? Or do I update it all at once? If all at once, how do I stop it from not updating from partial beliefs? Do I update it based on old beliefs?
* Seems to update just on the evidence of the neighbors, this is unchanging.
If the agent choose bandit arm A, can they still listen to their neighbors and update their beliefs?

## Thoughts
* Could extend the model, she currently updates on beliefs, could update on evidence only
* Additionally, with high trust in "domain expert" could take the stated belief as fact (the agent updates their own belief fully to match). This would converge on the ideas very quickly.