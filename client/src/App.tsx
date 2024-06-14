import { useState } from 'react'
import './App.css'
import { Button } from "@/components/ui/button"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <Button className="hover:bg-secondary/20" variant="secondary">Información</Button>
        <div className="p-4 w-screen">
          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>Is it accessible?</AccordionTrigger>
              <AccordionContent>
                Yes. It adheres to the WAI-ARIA design pattern.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </>
  )
}

export default App
