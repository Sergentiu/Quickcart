from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from shop.models import Product, Category  # Only Product and Category are in shop.models
from cart.models import Order, OrderItem    # Order and OrderItem are in cart.models

# Content-Based Filtering: Recommends products based on description and category similarity
def get_product_recommendations(product_name, num_recommendations=5):
    """
    Returns a list of product names similar to the given product_name based on TF-IDF similarity.
    Uses product description and category as features.
    """
    # Fetch all available products
    products = Product.objects.filter(available=True)
    if not products.exists():
        return []

    # Prepare data for vectorization
    product_data = []
    for product in products:
        category_name = product.category.name if product.category else "Uncategorized"
        text = f"{category_name} {product.description}"
        product_data.append({"id": product.id, "name": product.name, "text": text})

    df = pd.DataFrame(product_data)

    # Vectorize the text data using TF-IDF
    tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = tfidf.fit_transform(df["text"])

    # Find the target product
    target_product = df[df["name"].str.lower() == product_name.lower()]
    if target_product.empty:
        return []

    target_idx = target_product.index[0]
    target_vector = tfidf_matrix[target_idx]

    # Compute cosine similarity
    cosine_sim = cosine_similarity(target_vector, tfidf_matrix).flatten()

    # Get top similar products (excluding the target itself)
    similar_indices = cosine_sim.argsort()[-num_recommendations-1:-1][::-1]
    recommended_products = df.iloc[similar_indices]["name"].tolist()

    return recommended_products

# Collaborative Filtering: Recommends products based on user purchase history
def get_collaborative_recommendations(user_id, num_recommendations=5):
    """
    Returns a list of product names recommended for the given user_id based on order history.
    Uses SVD from the surprise library with quantity as a proxy for rating.
    """
    # Fetch completed order data
    orders = OrderItem.objects.select_related('order', 'product').filter(order__status='completed')
    if not orders.exists():
        return []

    # Prepare data for Surprise (user_id, product_id, rating)
    data = [(oi.order.user_id, oi.product_id, oi.quantity) for oi in orders]
    df = pd.DataFrame(data, columns=['user_id', 'product_id', 'rating'])

    # Define rating scale (assuming quantity as a proxy; max is 10 from AddToCartForm)
    reader = Reader(rating_scale=(1, 10))
    dataset = Dataset.load_from_df(df, reader)

    # Use full dataset for training (no test split for simplicity)
    trainset = dataset.build_full_trainset()

    # Train SVD model
    algo = SVD()
    algo.fit(trainset)

    # Get all available product IDs
    all_product_ids = Product.objects.filter(available=True).values_list('id', flat=True)

    # Predict ratings for the user for all products
    predictions = [algo.predict(user_id, pid) for pid in all_product_ids]
    predictions.sort(key=lambda x: x.est, reverse=True)  # Sort by estimated rating

    # Get top product IDs and map to names
    top_product_ids = [pred.iid for pred in predictions[:num_recommendations]]
    recommended_products = Product.objects.filter(id__in=top_product_ids).values_list('name', flat=True)

    return list(recommended_products)