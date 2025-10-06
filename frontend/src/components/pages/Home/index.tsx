import "./index.scss";
import Card from "../../utilities/Card";
import { useEffect } from "react";
import { getProducts } from "../../../lib/requestUtils";
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "../../../composables/api";
import PromotionsCarousel from "../../layout/PromotionsCarousel";

export default function Home() {
  const { data: products, isLoading: loadingProducts } = useQuery({
    queryKey: ['products', 'all'],
    queryFn: getProducts,
    staleTime: Infinity
  })
  useEffect(() => {

    fetchData("categories")
      .then((res) => res.json())
      .then(data => {
        console.log(data)
      })


  }, [])




  return <>
    <section className="carousel">
        <PromotionsCarousel />
    </section>



    <section className="products">
      <h2 className="products-title">Trending Products</h2>


      <ul className="products-list">
        {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
         loadingProducts ? "Loading" : products?.map((product: any) => {
          return <li className="products-li" key={product.id}><Card productData={product}/></li>
        }) }
        
        {/* <li className="products-li"><Card /></li>
        <li className="products-li"><Card /></li>
        <li className="products-li"><Card /></li> */}
      </ul>
    </section>
  </>


}

