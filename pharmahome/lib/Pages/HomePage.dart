import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Future<List<Product>> fetchProducts() async {
    final response = await http.get(Uri.parse('https://your-api-endpoint.com/products'));

    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((product) => Product.fromJson(product)).toList();
    } else {
      throw Exception('Failed to load products');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PharmaHome'),
        leading: Builder(
          builder: (context) => IconButton(
            icon: Icon(Icons.menu),
            onPressed: () => Scaffold.of(context).openDrawer(),
          ),
        ),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.green,
              ),
              child: Container(
                child: Text(
                  'Menu',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.w700,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            ListTile(
              leading: Icon(Icons.home),
              title: Text('Accueil'),
              onTap: () {
                // Action when this menu item is tapped
              },
            ),
            ListTile(
              leading: Icon(Icons.category),
              title: Text('Catégories'),
              onTap: () {
                // Action when this menu item is tapped
              },
            ),
            ListTile(
              leading: Icon(Icons.book),
              title: Text('Conseil'),
              onTap: () {
                // Action when this menu item is tapped
              },
            ),
            // Add more ListTile widgets here for more menu items
          ],
        ),
      ),
      body: FutureBuilder<List<Product>>(
        future: fetchProducts(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            List<Product> products = snapshot.data!;
            return SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  SectionTitle(title: 'Produits Favoris'),
                  FavoriteProductsCarousel(products: products),
                  SectionTitle(title: 'Catégories'),
                  ProductCategories(products: products),
                ],
              ),
            );
          } else if (snapshot.hasError) {
            return Center(child: Text("Erreur: ${snapshot.error}"));
          }
          return Center(child: CircularProgressIndicator());
        },
      ),
    );
  }
}

class SectionTitle extends StatelessWidget {
  final String title;

  SectionTitle({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

class FavoriteProductsCarousel extends StatelessWidget {
  final List<Product> products;

  FavoriteProductsCarousel({required this.products});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      child: ListView(
        scrollDirection: Axis.horizontal,
        children: products.map((product) => ProductCard(product: product)).toList(),
      ),
    );
  }
}

class ProductCard extends StatelessWidget {
  final Product product;

  ProductCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      margin: EdgeInsets.all(8.0),
      color: Colors.blueAccent,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Text(
            product.name,
            style: TextStyle(color: Colors.white),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              IconButton(
                icon: Icon(Icons.add_shopping_cart, color: Colors.white),
                onPressed: () {
                  // Action to add to cart
                },
              ),
              IconButton(
                icon: Icon(Icons.favorite, color: Colors.white),
                onPressed: () {
                  // Action to add to favorites
                },
              ),
            ],
          ),
          TextButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => ProductDetailsPage(product: product)),
              );
            },
            child: Text('Voir Détails', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}

class ProductCategories extends StatelessWidget {
  final List<Product> products;

  ProductCategories({required this.products});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: products.map((product) => CategoryCard(product: product)).toList(),
    );
  }
}

class CategoryCard extends StatelessWidget {
  final Product product;

  CategoryCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(8.0),
      padding: EdgeInsets.all(16.0),
      color: Colors.greenAccent,
      child: Row(
        children: <Widget>[
          Icon(Icons.category),
          SizedBox(width: 8.0),
          Text(product.category),
        ],
      ),
    );
  }
}

class ProductDetailsPage extends StatelessWidget {
  final Product product;

  ProductDetailsPage({required this.product});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(product.name),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text(
              product.name,
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16.0),
            Text(
              product.description,
              style: TextStyle(fontSize: 16),
            ),
            // Add more details and styling as needed
          ],
        ),
      ),
    );
  }
}

class Product {
  final String name;
  final String category;
  final String description;

  Product({required this.name, required this.category, required this.description});

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      name: json['name'],
      category: json['category'],
      description: json['description'],
    );
  }
}
