from colorama import deinit
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
from torch import cuda_version


def sim(sentence1, sentence2):
    
    model = SentenceTransformer('all-mpnet-base-v2', device="cuda")

    #Compute embedding for both lists
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    return cosine_scores



print (sim("triple bed is better than single bed for me","double bed is not better than single bed for me"))

print("test git hub commit")
